import os

namesfilepath = "names.txt"

if os.path.exists(namesfilepath):
    with open(namesfilepath, "r") as file_obj:
        names = file_obj.readlines()  # Read all lines into a list

    print("".join(names))  
    print(f"There are {len(names)} names in the file.")

else:
    print(f"Error: '{namesfilepath}' does not exist.")
