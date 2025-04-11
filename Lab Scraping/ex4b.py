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

#find columns related to vehicles and fuel sources
vehicle_cols = [col for col in df.columns if 'vehicle' in col.lower()
or 'make' in col.lower() or 'model' in col.lower()]
fuel_cols = [col for col in df.columns if 'fuel' in col.lower()]

print("\nPotential vehicle-related columns: ", vehicle_cols)
print("Potential fuel-related columns: ", fuel_cols)

#if we find appropriate columns, we can proceed with the analysis
if vehicle_cols and fuel_cols:
    vehicle_col = vehicle_cols[0]
    fuel_col = fuel_cols[0]

    print(f"\n First 10 entries of {vehicle_col} and {fuel_cols}:")
    print(df[[vehicle_col,fuel_col]].head(10))

    print("\nVehicle count by type and fuel source: ")
    print(df.groupby([vehicle_col, fuel_col]).size().reset_index(name='count'))
#most common vehicle/fuel combinations
    print("\nMost common vehicle combos:")
    print(df.groupby([vehicle_col, fuel_col]).size().nlargest(5))
else:
    print("Required columns 'vehicle' and 'fuel_source' not found in the dataset.")
    print(df.head(3))