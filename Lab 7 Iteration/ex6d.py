data = ("hello", 10, "goodbye", 3, "goodnight", 5)
data_list = list(data)
user_input = input("Enter a value to append the tupple: ")

data_list.append(user_input)

data = tuple(data_list)

print("Appended tuple: ", data)