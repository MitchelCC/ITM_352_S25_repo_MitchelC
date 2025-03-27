import pandas as pd

file_id = "1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

print(df.head())