even_numbers = []
number = 2 

while not even_numbers or even_numbers[-1] <= 50: 
    even_numbers.append(number)
    number += 2

if even_numbers[-1] > 50:
    even_numbers.pop() 

print(even_numbers)