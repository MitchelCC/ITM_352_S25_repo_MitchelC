import pandas as pd
from sodapy import Socrata

# Setting up API client
client = Socrata("data.cityofchicago.org", None)  

# Retrieve first 500 records from the vehicle licenses dataset
results = client.get("rr23-ymwb", limit=500)

# Convert to DataFrame
df = pd.DataFrame.from_records(results)

print("Available columns:")
print(df.columns.tolist())

fuel_col = None
possible_fuel_columns = ['fuel_type',  'fuel_source', 'fuel', 'fuel_code', 'primary_fuel']

for col in possible_fuel_columns:
    if col in df.columns:
        fuel_col = col
        break
if fuel_col:
    fuel_counts = df[fuel_col].value_counts().reset_index()
    fuel_counts.columns = ['Fuel Type', 'Number of Vehicles']

    print("\nNumber of vehicles per fuel type: ")
    print(fuel_counts)

    