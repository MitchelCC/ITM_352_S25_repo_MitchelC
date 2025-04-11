import requests
import pandas as pd 

url = "https://data.cityofchicago.org/resource/97wa-y6ff.json"
params = {
        "$select": "driver_type,count(license)",
        "$group": "driver_type"
    }
    
try:
        #grabbing data
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)

    df = df.rename(columns={"count_license": "count"})

    df['count'] = pd.to_numeric(df['count'], errors='coerce')
    df = df.set_index('driver_type')

        # Print the formatted DataFrame
    print("License Counts by Driver Type:")
    print("-" * 40)
    print(df)
    print("-" * 40)
    
    # Print DataFrame info
    print("\nDataFrame Info:")
    print(f"Shape: {df.shape}")
    print(f"Index: {df.index.name}")
    print("Columns:", df.columns.tolist())

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError as e:
    print(f"Data processing error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")