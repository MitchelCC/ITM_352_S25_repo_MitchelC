import pandas as pd

file_id = "1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"
url = f"https://drive.google.com/uc?id={file_id}"

try:
    df = pd.read_csv(url_engine = 'pyarrow', on_bad_lines='skip')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    print(df.head())

except Exception as e: 
    print(f"Error reading the file: {e}")