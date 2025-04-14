import csv

count = 0
total = 0.0
max_inc = None
min_inc = None

with open('survey_1000.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 5456:
            realinc_str = row[5456].strip()
            if realinc_str:
                try:
                    realinc = float(realinc_str)
                    if realinc > 0:
                        count += 1
                        total += realinc
                        if max_inc is None or realinc > max_inc:
                            max_inc = realinc
                        if min_inc is None or realinc < min_inc:
                            min_inc = realinc
                except ValueError:
                    pass  # Skip invalid entries

average = total / count if count > 0 else 0

print(f"Number of values > 0: {count}")
print(f"Average REALINC: {average:.2f}")
print(f"Maximum REALINC: {max_inc if max_inc is not None else 'N/A'}")
print(f"Minimum REALINC: {min_inc if min_inc is not None else 'N/A'}")