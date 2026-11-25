# Reflection Questions:
# 1. Drop feels the most ambiguous to me because I would need to know and understand which columns to target. Information like whether it 
#    is an essential identifier would help me make the decision.
# 2. After some slight revisions, someone reading the script would probably understand each comment explaining why each decision was made.
# 3. Something important I did not expect from this dataset was a negative revenue. It informed me that negative revenues may exist to 
#    represent returns that commonly happen in the real world.

print("--- Exercise 1: Inspect ---")

import pandas as pd

df = pd.read_csv('data/messy_sales.csv')
df.info()
print(df.isnull().sum())

# Data quality issues:
# 1. Column "Unit Price" is dtype string but should be float
# 2. Column "Quantity Sold" is dtype float but should be integer
# 3. Column "Customer ID" has approximately 7.54% missing

print("\n--- Exercise 2: Standardize Column Names ---")

df.columns = df.columns.str.lower().str.replace(' ', '_')
print(df.columns.tolist())

print("\n--- Exercise 3: Handle Missing Values ---")

before = df.shape

df['quantity_sold'] = df['quantity_sold'].fillna(df['quantity_sold'].mean())
# Fill sections missing quantity_sold with mean, preserves number of rows and does not shift the column's average
df = df.dropna(subset=['order_id', 'order_date'])
# Drop rows with no order_id or order_date because there is no way to place the order

after = df.shape

print(f"Before: {before}\nAfter: {after}")

print(df.isnull().sum()) # order_id, order_date, and quantity_sold should be 0

print("\n--- Exercise 4: Fix Types ---")

df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
null_dates = df['order_date'].isnull().sum()
print(f"{null_dates} dates became NaT")

df['unit_price'] = df['unit_price'].str.replace('$', '', regex=False)
df['unit_price'] = df['unit_price'].str.replace(',', '', regex=False).astype(float)

df['quantity_sold'] = df['quantity_sold'].astype(int)

df['revenue'] = (df['unit_price'] * df['quantity_sold']).round(2)

print(df.dtypes)

print("\n--- Exercise 5: Check Duplicates ---")

print(f"Duplicate rows before: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Duplicate rows after: {df.duplicated().sum()}")

print("\n--- Exercise 6: Describe ---")

print(f"Before:\n{df.describe()}")

# Statistics that look suspicious:
# 1. The minimum revenue is negative
# 2. The maximum quantity_sold is 9,999
# 3. The maximum unit_price is absurdly high (could be contributing to the absurdly high maximum revenue and large difference 
#    between mean and median in unit_price and revenue)

# Keep negative revenues because they represent returns (money that went back to customers)

df = df[df['quantity_sold'] < 9999]
# Remove rows where quantity_sold is 9,999 because it is a placeholder, not a real order
# May also change values in revenue because revenue = unit_price * quantity_sold

# The absurdly high maximum unit_price could either be a data entry error or an outlier (would need additional information before making decision)

print(f"\nAfter:\n{df.describe()}")

print("\n--- Exercise 7: Save ---")

df.to_csv('data/clean_sales.csv', index=False)

df = pd.read_csv('data/clean_sales.csv')
df.info()
print("\n")
df = pd.read_csv('data/clean_sales.csv', parse_dates=['order_date'])
df.info()