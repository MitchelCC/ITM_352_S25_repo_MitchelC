#Exercise 2.3
#Asked the user to enter a number, then we turn it into float so we can receive decimals. 
input = float(input("Enter a decimal number between 1-100: "))
squared = round(input ** 2, 4) 
print(f"You entered the number {input} and the square of that number is {squared}")