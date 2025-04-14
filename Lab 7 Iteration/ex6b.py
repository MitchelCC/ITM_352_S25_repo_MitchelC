data = ("hello", 10, "goodbye", 3, "goodnight", 5)

try: 
    data.append("new_element")
except AttributeError as e:
    print("An attempt was made to append a value to the tuple, tuples are immutable.")
    print(f"Error: {e}")

    new_data = data + ("new_element",)
    print("A new tuple was create with the appended value: ")
    print(new_data)