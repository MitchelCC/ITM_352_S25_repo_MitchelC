import requests
from bs4 import BeautifulSoup

# Retrieve the mortgage rates page
url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
response = requests.get(url)
response.raise_for_status()  # Check for HTTP errors

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the rate table - looking for the table with lender and rate information
rate_table = soup.find('table')

# Extract each row from the table
rows = []
if rate_table:
    for row in rate_table.find_all('tr'):
        # Extract text from each cell in the row
        cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if cells:  # Skip empty rows
            rows.append(cells)
else:
    print("Could not find the rate table on the page")

# Display the extracted rows
print("Extracted Mortgage Rate Table Rows:")
for i, row in enumerate(rows):
    print(f"Row {i+1}: {row}")