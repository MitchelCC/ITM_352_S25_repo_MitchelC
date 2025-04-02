import pandas as pd
import numpy as np

try: 
    df = pd.read_csv(
        "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K",
        engine='pyarrow',
        dtype_backend='pyarrow',
        on_bad_lines='skip'
    )
except Exception as e: 
    print(f"Error reading the file: {e}")
    raise

df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

pd.set_option('display.max_columns', None) 

print(df)

#convert columns to numeric 
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

#compute sales column
df['sales'] = df['quantity'] * df['unit_price']

#create pivot table with numpy sum
pivot = df.pivot_table(
    index='region',
    columns='order_type',
    values='sales',
    aggfunc=np.sum,
)
#margin column
pivot['margins'] = np.sum(pivot[['Retail','Wholesale']], axis=1)

print('\nFirst 5 rows from Problem 1: ')
print(df.head())

print('\nPivot table:')
print(pivot)