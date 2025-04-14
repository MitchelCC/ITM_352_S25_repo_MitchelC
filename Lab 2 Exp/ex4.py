#Exercise 2.4
#Asked the user to enter a number, then we turn it into float so we can receive decimals. 
input = float(input("Enter a decimal number between 1-100: "))
squared = input ** 2 
print(f"You entered the number {input} and the square of that number is {round(squared, 2)}")