import pandas as pd

file_id = "1M-X_bypJJ6K5p6eM6aYBwt1qIizIiIex"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

df['units'] = pd.to_numeric(df['units'], errors='coerce')
df['sales price'] = pd.to_numeric(df['sales price'], errors='coerce')
df['land_sqft'] = pd.to_numeric(df['land_sqft'], errors='coerce')
df['gross_sqft'] = pd.to_numeric(df['gross_sqft'], errors='coerce')

df_filtered = df[df['units'] >= 500]

#drops unneccesary columns
df_filtered = df_filtered.drop(columns=['id','borough','easemeent'])
df_filtered = df_filtered.dropna()
df_filtered = df_filtered.drop_duplicates()
#print(df_filtered.head())

print(df_filtered.head())