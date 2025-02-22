import pandas as pd
import numpy as np

def load_data(file_path='data/raw/BrentOilPrices.csv'):
    """Load and preprocess Brent oil prices data."""
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
    df = df.sort_values('Date').set_index('Date')
    return df

def preprocess_data(df):
    """Handle missing values and calculate log returns."""
    # Forward-fill missing values (e.g., weekends/holidays)
    df = df.ffill()
    
    # Compute daily log returns for stationarity
    df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
    df = df.dropna()
    
    return df

if __name__ == "__main__":
    # Example usage
    df = load_data()
    df_clean = preprocess_data(df)
    df_clean.to_csv('data/Processed/processed_data.csv')
    print("Data preprocessing complete. Cleaned data saved to data/processed_data.csv.")