import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import requests

# Set up the file download
file_id = "1-kjcJHN_pCJfB-f3_2xgQNF5U-5PitjU"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Download and parse the JSON data
response = requests.get(url)
data = [json.loads(line) for line in response.text.split('\n') if line.strip()]

# Create DataFrame using json_normalize to handle nested structures
df = pd.json_normalize(data)

# Find the correct column names (they might be nested)
pickup_col = next((col for col in df.columns if 'pickup_community_area' in col), None)
dropoff_col = next((col for col in df.columns if 'dropoff_community_area' in col), None)

if pickup_col and dropoff_col:
    # Filter out records with missing community area data
    df = df.dropna(subset=[pickup_col, dropoff_col])
    
    # Convert to integers, handling any string formatting
    df[pickup_col] = pd.to_numeric(df[pickup_col].astype(str).str.extract(r'(\d+)')[0], errors='coerce').astype('Int64')
    df[dropoff_col] = pd.to_numeric(df[dropoff_col].astype(str).str.extract(r'(\d+)')[0], errors='coerce').astype('Int64')
    
    # Create the crosstab matrix
    cross_tab = pd.crosstab(df[pickup_col], df[dropoff_col])
    
    # Create the heatmap visualization
    plt.figure(figsize=(15, 12))
    sns.heatmap(cross_tab, 
                cmap="YlOrRd",
                annot=False,
                fmt='d',
                square=True,
                cbar_kws={'label': 'Number of Trips'})
    
    plt.title('Chicago Taxi Trips - July 7, 2017\nPickup vs Dropoff Community Areas', pad=20)
    plt.xlabel('Dropoff Community Area', labelpad=10)
    plt.ylabel('Pickup Community Area', labelpad=10)
    plt.tight_layout()
    plt.show()
else:
    print("Error: Could not find required columns in the data.")
    print("Available columns:", df.columns.tolist())
    print("First row sample:", df.iloc[0].to_dict() if len(df) > 0 else "No data")