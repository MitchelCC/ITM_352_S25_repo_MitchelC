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
    aggfunc=[np.sum, np.mean]
)
#margin column
pivot[('margins', 'sum')] = pivot[('sum','Retail',)], + pivot[('sum','Wholesale',)]

#reorder columns to group by retail/wholesale with sum/mean sub-columns
pivot = pivot [[('sum', 'Retail'), ('mean', 'Retail'), ('sum', 'Wholesale'), ('mean', 'Wholesale'), ('margins', 'sum')]]

#format output to 2 decimals with currency
pd.set_option('display.float_format', '{:,.2f}'.format)

print('\nPivot table with averges and totals:')
print(pivot)