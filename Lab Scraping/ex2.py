import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202410"

try:
    tables = pd.read_html(url)
    if len(tables) > 0:
        df = tables[0]
        
        print("Columns in the interest rate table: ")
        print(df.columns.tolist())

        print(df.head())
    else:
        print("No tables found on the page.")
except Exception as e:
    print(f"An error occurred: {e}")

