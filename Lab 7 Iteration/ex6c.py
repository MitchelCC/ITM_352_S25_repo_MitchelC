data = ("hello", 10, "goodbye", 3, "goodnight", 5)

user_input = input("Enter a value to append the tupple: ")

data = (*data, user_input)

print("Appended tuple: ", data)