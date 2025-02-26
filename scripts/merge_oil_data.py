# Import necessary libraries
import pandas as pd
import os

# Step 1: Load the Brent Oil Prices Data
# File: BrentOilPrices.csv
oil_prices_file = 'data/raw/BrentOilPrices.csv'
oil_prices = pd.read_csv(oil_prices_file, parse_dates=['Date'], dayfirst=True)
oil_prices.set_index('Date', inplace=True)

# Display the first few rows of the oil prices data
print("Brent Oil Prices Data:")
print(oil_prices.head())

# Step 2: Load the Merged Additional Factors Data
# File: merged_data.csv (output from Task 1)
additional_factors_file = 'data/external/merged_data.csv'
additional_factors = pd.read_csv(additional_factors_file, parse_dates=['Date'])
additional_factors.set_index('Date', inplace=True)

# Display the first few rows of the additional factors data
print("\nMerged Additional Factors Data:")
print(additional_factors.head())

# Step 3: Merge the Datasets on 'Date'
# Use a left join to ensure all dates from the oil prices dataset are retained
merged_dataset = oil_prices.join(additional_factors, how='left')

# Handle missing values (optional)
# Forward-fill missing values
merged_dataset.ffill(inplace=True)

# Backward-fill remaining missing values
merged_dataset.bfill(inplace=True)

# Convert relevant columns to numeric types
numeric_columns = ['GDP_Growth', 'Inflation', 'USD_to_EUR']
for col in numeric_columns:
    if col in merged_dataset.columns:
        merged_dataset[col] = pd.to_numeric(merged_dataset[col], errors='coerce')

# Step 4: Validate the Merged Dataset
# Check for missing values
print("\nMissing Values in Merged Dataset:")
print(merged_dataset.isnull().sum())

# Check data types
print("\nData Types in Merged Dataset:")
print(merged_dataset.dtypes)

# Check date range
print("\nDate Range:")
print(f"Start Date: {merged_dataset.index.min()}")
print(f"End Date: {merged_dataset.index.max()}")

# Display the first few rows of the merged dataset
print("\nMerged Dataset:")
print(merged_dataset.head())

# Step 5: Save the Merged Dataset
# Define the output directory
output_dir = 'data/processed'
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Save the merged dataset to a CSV file
output_file = f'{output_dir}/merged_oil_data.csv'
merged_dataset.to_csv(output_file)

print(f"\nMerged dataset saved to: {output_file}")