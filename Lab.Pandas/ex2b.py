import pandas as pd

ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]

#Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]


age_gender = list(zip(ages, gender))

df = pd.DataFrame(age_gender, index=names, columns=['Age', 'Gender'])
print('DataFrame: ')
print(df)
print('\nSummary Statistics: ')
print(df.describe(include='all'))

