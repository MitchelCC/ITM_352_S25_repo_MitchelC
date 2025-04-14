import pandas as pd

data = pd.read_csv("taxi_1000.csv")

data_filtered = data[data['Fare'] > 10]

total_fares = data_filtered['Fare'].sum()

average_fare = total_fares / len(data_filtered)

max_trip_dist = data_filtered['Trip Miles'].max()

print(f"Total of all fares for trips with fares > $10: ${total_fares:.2f}")
print(f"Average fare for trips with fares > $10: ${average_fare:.2f}")
print(f"Maximum trip distance for trips with fares > $10: {max_trip_dist:.2f} miles")