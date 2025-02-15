#asking user to input first name, middle initial, and last name
first = input("Enter first name: ")
middle = input("Enter middle initial: ")
last = input("Enter last name: ")

names = [first, middle, last]

FullName = "{} {}. {}". format(names)

print(f"You full name is {FullName}")
