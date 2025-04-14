data = ("hello", 10, "goodbye", 3, "goodnight", 5)

string_count = 0 
for element in data: 
    if isinstance(element, str): 
        string_count += 1

print(f"There are {string_count} strings in the tuple")

user_input = input("Enter a value to append the tupple: ")

new_data = data + (user_input,)

print("Appended tuple: ", new_data)

new_string_count = 0
for element in new_data: 
    if isinstance(element, str): 
        new_string_count += 1
print(f"There are {new_string_count} strings in the new tuple")