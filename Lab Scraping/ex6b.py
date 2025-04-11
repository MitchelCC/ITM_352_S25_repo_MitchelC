import requests
from bs4 import BeautifulSoup

def get_hawaii_mortgage_rates():
    url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print("Attempting to fetch mortgage rates...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"HTTP Status Code: {response.status_code}")
        
        response.raise_for_status()
        
        print("Parsing HTML content...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debug: Save HTML for inspection
        with open('page_content.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("Saved page content to 'page_content.html' for inspection")
        
        # Try to find tables - let's see all tables first
        all_tables = soup.find_all('table')
        print(f"Found {len(all_tables)} tables on the page")
        
        if not all_tables:
            print("No tables found in the page content")
            return
            
        # Look for the rates table (this might need adjustment)
        rate_table = None
        for i, table in enumerate(all_tables):
            if 'mortgage' in str(table).lower() or 'rate' in str(table).lower():
                rate_table = table
                print(f"Found potential rates table at index {i}")
                break
                
        if not rate_table:
            print("Could not identify the rates table - checking all tables")
            rate_table = all_tables[0]  # Fallback to first table
            
        # Extract data from the table
        print("\nExtracted Mortgage Rates:")
        print("="*50)
        for row in rate_table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if cells:
                print(" | ".join(cells))
        print("="*50)
        
    except requests.exceptions.RequestException as e:
        print(f"\nRequest failed: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}")

# Execute the function
get_hawaii_mortgage_rates()