# Import necessary libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access API keys from environment variables
FRED_API_KEY = os.getenv('FRED_API_KEY')
NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY')
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')

# Set plotting style
pd.set_option('display.max_columns', None)

# Step 1: Collect Economic Indicators

## GDP Growth Rates (FRED API)
def fetch_gdp_data(api_key):
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={api_key}&file_type=json'
    response = requests.get(url)
    data = response.json()
    gdp_data = [(obs['date'], obs['value']) for obs in data['observations']]
    return pd.DataFrame(gdp_data, columns=['Date', 'GDP_Growth'])

gdp_df = fetch_gdp_data(api_key=FRED_API_KEY)
gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])

## Inflation Rates (World Bank API)
def fetch_inflation_data(country_code='US', indicator_code='FP.CPI.TOTL.ZG'):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json'
    response = requests.get(url)
    data = response.json()
    inflation_data = [(year['date'], year['value']) for year in data[1]]
    return pd.DataFrame(inflation_data, columns=['Date', 'Inflation'])

inflation_df = fetch_inflation_data()
inflation_df['Date'] = pd.to_datetime(inflation_df['Date'])

## Exchange Rates (FRED API for Historical EUR/USD)
def fetch_exchange_rate_fred(api_key):
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id=DEXUSEU&api_key={api_key}&file_type=json'
    response = requests.get(url)
    data = response.json()
    exchange_data = [(obs['date'], obs['value']) for obs in data['observations']]
    return pd.DataFrame(exchange_data, columns=['Date', 'USD_to_EUR'])

exchange_rate_df = fetch_exchange_rate_fred(api_key=FRED_API_KEY)
exchange_rate_df['Date'] = pd.to_datetime(exchange_rate_df['Date'])

# Step 2: Collect Geopolitical Events

## News Articles (NewsAPI)
def fetch_geopolitical_events(api_key, query='oil AND geopolitical'):
    newsapi = NewsApiClient(api_key=api_key)
    try:
        # Use 'relevancy' as the correct sort_by parameter
        articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        event_data = [(article['publishedAt'][:10], article['title']) for article in articles['articles']]
        return pd.DataFrame(event_data, columns=['Date', 'Geopolitical_Event'])
    except Exception as e:
        print(f"Error fetching geopolitical events: {e}")
        return pd.DataFrame(columns=['Date', 'Geopolitical_Event'])

geopolitical_df = fetch_geopolitical_events(api_key=NEWSAPI_API_KEY)
geopolitical_df['Date'] = pd.to_datetime(geopolitical_df['Date'])

# Step 3: Collect OPEC Policies

## Scrape OPEC Website
def scrape_opec_policies():
    url = "https://www.opec.org/opec_web/en/news_center/press_releases.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    press_releases = []
    for item in soup.select('.press_release_item'):
        title = item.find('h3').text.strip()
        date = item.find('span').text.strip()
        press_releases.append((date, title))
    return pd.DataFrame(press_releases, columns=['Date', 'OPEC_Policy'])

opec_df = scrape_opec_policies()
opec_df['Date'] = pd.to_datetime(opec_df['Date'], format='%d %B %Y')

# Step 4: Merge All Datasets

# Create a base DataFrame for merging
base_date_range = pd.date_range(start="1987-05-20", end="2022-09-30", freq='D')
base_df = pd.DataFrame(base_date_range, columns=['Date'])

# Merge datasets on 'Date'
merged_df = base_df.merge(gdp_df, on='Date', how='left')
merged_df = merged_df.merge(inflation_df, on='Date', how='left')
merged_df = merged_df.merge(exchange_rate_df, on='Date', how='left')
merged_df = merged_df.merge(geopolitical_df, on='Date', how='left')
merged_df = merged_df.merge(opec_df, on='Date', how='left')

# Step 5: Data Processing

## Handle Missing Values
# Forward-fill missing values
merged_df.ffill(inplace=True)

# Backward-fill remaining missing values
merged_df.bfill(inplace=True)

# Replace NaNs in specific columns with placeholders
merged_df['Geopolitical_Event'].fillna('No Event', inplace=True)
merged_df['OPEC_Policy'].fillna('No Policy Update', inplace=True)

# Infer correct data types
merged_df = merged_df.infer_objects()

## Convert Data Types
merged_df['GDP_Growth'] = pd.to_numeric(merged_df['GDP_Growth'], errors='coerce')
merged_df['Inflation'] = pd.to_numeric(merged_df['Inflation'], errors='coerce')
merged_df['USD_to_EUR'] = pd.to_numeric(merged_df['USD_to_EUR'], errors='coerce')

# Drop rows with too many NaNs (optional)
merged_df.dropna(thresh=len(merged_df.columns) - 2, inplace=True)  # Keep rows with at least 2 non-NaN values

# Step 6: Save to CSV File
output_dir = 'data/external'
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
merged_df.to_csv(f'{output_dir}/merged_data.csv', index=False)

# Step 7: Display the Final DataFrame
print("Final Merged DataFrame:")
print(merged_df.head())