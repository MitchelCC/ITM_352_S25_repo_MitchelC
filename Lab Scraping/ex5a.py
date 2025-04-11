import requests

url = "https://data.cityofchicago.org/resource/97wa-y6ff.json"
params = {
    '$select' : 'driver_type,count(license)',
    'group' : 'driver_type'
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    print(data)

    print ('\nData format analysis: ')
    print(f'Type of response: {type(data)}')
    if isinstance (data, list) and len(data) > 0:
        print(f"Type of first element: {type(data[0])}")
        print("First record of structure: ", data[0])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)