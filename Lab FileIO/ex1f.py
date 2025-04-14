import os

namesfilepath = "names.txt"

if os.path.exists(namesfilepath):
    with open(namesfilepath, "a") as file_obj:
        file_obj.write("\nPort, Dan")

    with open(namesfilepath, "r") as file_obj:
        names = file_obj.readlines()  # Read all lines into a list

    print("Updated file contents: ")
    print("".join(names))  
    print(f"There are {len(names)} names in the file.")

else:
    print(f"Error: '{namesfilepath}' does not exist.")
