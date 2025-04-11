import pandas as pd
from sodapy import Socrata

# Setting up API client
client = Socrata("data.cityofchicago.org", None)  

# Retrieve first 500 records from the vehicle licenses dataset
results = client.get("rr23-ymwb", limit=500)

# Convert to DataFrame
df = pd.DataFrame.from_records(results)

# Inspect the data
print("First 5 records:")
print(df.head())
print("\nDataFrame shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nBasic info:")
print(df.info())

