import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import for 3D plotting
import requests


file_id = '1-kvj2Ore88PGzZ9J7_lPBOvNf5C1ohpQ'
url = f'https://drive.google.com/uc?export=download&id={file_id}'

try:
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    
    # Load the JSON data directly from the response
    trips = json.loads(response.text)
    
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Prepare data for plotting
miles = []
fares = []
dropoff_areas = []

for trip in trips:
    # filteriing out trips with 0 miles and missing data
    if (float(trip['trip_miles']) > 0 and 
        'fare' in trip and 
        'dropoff_community_area' in trip and
        trip['dropoff_community_area'] is not None):
        
        miles.append(float(trip['trip_miles']))
        fares.append(float(trip['fare']))
        dropoff_areas.append(int(trip['dropoff_community_area']))# Create 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Create the scatter plot
scatter = ax.scatter(miles, dropoff_areas, fares, c=fares, cmap='viridis', alpha=0.6)

# Add labels and title
ax.set_xlabel('Trip Miles')
ax.set_ylabel('Dropoff Area')
ax.set_zlabel('Fare ($)')
ax.set_title('3D Visualization: Fares by Trip Miles and Dropoff Area (From Area 8)')

# Add colorbar
cbar = fig.colorbar(scatter, shrink=0.5, aspect=5)
cbar.set_label('Fare ($)')

ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()