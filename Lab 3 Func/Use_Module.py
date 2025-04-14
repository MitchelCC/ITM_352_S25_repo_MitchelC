import HandyMath
n1 = float(input("Enter number 1: "))
n2 = float(input("Enter number 2: "))

print(f"The midpoint of {n1} and {n2} is {HandyMath.midpoint(n1,n2)}")

print(f"The square root of the square of {n2} is {HandyMath.squareroot(n2 **2)}")

print(f"{n1} raised to the exponent of {n2} is {HandyMath.exponent(n1, n2)}")

print(f"The maximum of {n1} and {n2} is {HandyMath.max_of_2(n1, n2)}")

print(f"The minimum of {n1} and {n2} is {HandyMath.min_of_2(n1, n2)}")