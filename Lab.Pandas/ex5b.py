import pandas as pd

file_id = "1M-X_bypJJ6K5p6eM6aYBwt1qIizIiIex"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

df['units'] = pd.to_numeric(df['units'], errors='coerce')

df_filtered = df[df['units'] >= 500]

print(df_filtered.head())

