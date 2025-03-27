import pandas as pd

url = "https://drive.google.com/file/d/1-MpDUIRZxhFnN-rcDdJQMe_mcCSciaus"
df = pd.read_json(url)

print(df.describe())

print(df)
#PRint the median for numerical columns
print("\nMedian values:")
print(df['fare'].median())