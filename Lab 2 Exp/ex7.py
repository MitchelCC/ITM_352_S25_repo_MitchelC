#Exercise 2.7
f_temp = float(input("Enter a temperature in the Fahrenheit temperature scale: "))
#convert f to c, formula (f - 32) * (5/9)
c_temp = (f_temp - 32) * (5/9)
print(f"You entered {f_temp}°F and that is equivalent to {c_temp}°C.")