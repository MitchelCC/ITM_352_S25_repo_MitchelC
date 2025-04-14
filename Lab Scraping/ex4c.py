import pandas as pd
from sodapy import Socrata

# Connect to Chicago's open data
client = Socrata("data.cityofchicago.org", None)

# Get first 500 records
results = client.get("rr23-ymwb", limit=500)
df = pd.DataFrame.from_records(results)

# Group by fuel type and count vehicles
fuel_counts = df['vehicle_fuel_source'].value_counts().reset_index()
fuel_counts.columns = ['Fuel Type', 'Vehicle Count']
print(fuel_counts.to_string(index=False))

