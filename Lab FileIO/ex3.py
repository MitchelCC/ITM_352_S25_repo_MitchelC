import pandas as pd

data = pd.read_csv("taxi_1000.csv")

fares = data['Fare'].sum()

avg_fare = fares / 1000

max_trip_dist = data['Trip Miles'].max()

print(f"Total fares: ${fares:.2f}")
print(f"Average fare: ${avg_fare:.2f}")
print(f"Maximum trip distance: {max_trip_dist:.2f} miles")