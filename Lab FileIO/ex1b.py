with open('names.txt', 'r') as file_obj:
    print(file_obj.read())
    file_obj.close()
print(type(file_obj))
