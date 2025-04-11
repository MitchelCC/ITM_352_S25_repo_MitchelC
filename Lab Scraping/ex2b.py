import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202410"

try:
    tables = pd.read_html(url)
    if len(tables) > 0:
        df = tables[0]

        df.columns = [col.striop() for col in df.columns]
        one_month_col = None
        for col in df.columns:
            if '1 mo' in col.lower():
                one_month_col = col
                break
        if one_month_col:
            print(f"\nDate\t\t{one_month_col}")
            print("---------------")

            for index, row in df.iterrows():
                print(f"{row['Date']}\t{row[one_month_col]}")
        else:
            print("1 Month column not found.")
except Exception as e:
    print(f"An error occurred: {e}")