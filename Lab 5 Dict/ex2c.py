
#Write Python code to define a list of taxi trip durations in miles (use values 1.1, 0.8, 2.5, 2.6). 

trip_durations = [1.1,0.8,2.5,2.6]
trip_fares = (6.25, 5.25, 10.50, 8.05)
trips = dict(zip(trip_durations, trip_fares))
print(trips)