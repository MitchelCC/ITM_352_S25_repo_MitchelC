#Exercise 2.6
#Asked the user to enter a weight in lbs, then we turn it into float so we can receive decimals.
user_lbs = input("Enter a weight in pounds: ")
#convert lbs to kgs 
kg =  float(user_lbs) * 0.453592
print(f"You entered the weight {user_lbs}(lbs) and that is equivalent to {kg} kilograms.")