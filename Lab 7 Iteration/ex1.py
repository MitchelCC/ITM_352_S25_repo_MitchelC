#Initialize empty list
odd_numb = []

for number in range (1, 51): 
    if number % 2 != 0:
        odd_numb.append(number)

print(odd_numb)