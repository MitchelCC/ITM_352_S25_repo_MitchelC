import requests

def get_driver_type_counts():
    url = "https://data.cityofchicago.org/resource/97wa-y6ff.json"
    params = {
        "$select": "driver_type,count(license)",
        "$group": "driver_type"
    }
    
    try:
        print("Making API request...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  
        data = response.json()
        
        if not data:
            print("No data returned from API")
            return
            
        print("\nSuccess! Received data in JSON format:")
        print("-" * 50)
        print(data)
        print("-" * 50)
        
        print("\nData format details:")
        print(f"Type of response: {type(data)}")
        print(f"Number of records: {len(data)}")
        print(f"First record type: {type(data[0])}")
        print("\nSample record:")
        print(data[0])
        
    except requests.exceptions.RequestException as e:
        print(f"\nError making request: {e}")
    except ValueError as e:
        print(f"\nError parsing JSON: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

# Execute the function
get_driver_type_counts()