import pandas as pd
import time
import sys
import os
import openpyxl

# Add all possible aliases for each column name
#this part was generated by AI. Previously, everytime I tried to run the code, it would have the output "error: sales_price"
#looking back at it now, I realize that the error was due to the fact that the column name was not normalized. 
#it was supposed to be "unit_price", not "sales_price".
COLUMN_MAPPING = {
    'sales_price': ['sales_price', 'sale_price', 'price','unit_price'],  
    'order_type': ['order_type', 'type'],
    'product_category': ['product_category', 'category']
}

req_fields = ['sales_region', 'order_type', 'customer_state', 
              'customer_type', 'product_category', 'quantity',
              'sales_price', 'employee_name']

menu_items = [("Show the first n rows of sales data", 'show_first_n_rows'),
    ("Total sales by region and order_type", 'total_sales_region_order_type'),
    ("Average sales by region with average sales by state and sale type", 'average_sales_region_state_sale_type'),
    ("Sales by customer type and order type by state", 'sales_customer_order_type_state'),
    ("Total sales quantity and price by region and product", 'total_sales_region_product'),
    ("Sales by region and product with percentages", 'sales_region_product_percentages'),
    ("Total sales quantity and price customer type", 'total_sales_customer_type'),
    ("Max and min sales price of sales by category", 'max_min_sales_category'),
    ("Number of unique employees by region", 'unique_employees_region'),
    ("Create a custom pivot table", 'create_custom_pivot'),
    ("Exit", 'exit_program')]

#handles exceptions and validates the DF
def handle_errors(func):
    def wrapper(df, *args, **kwargs):
        if df is None or df.empty:
            print("Error: DataFrame is empty or not loaded.")
            return None
        try:
            return func(df, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}. Available columns: {df.columns.tolist()}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    return wrapper

#normalizing column names based on mapping
def normalize_column(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    for standard_name, aliased_names in COLUMN_MAPPING.items():
        for alias in aliased_names:
            if alias in df.columns:
                df.rename(columns={alias: standard_name}, inplace=True)
    return df

#load sales data
def load_data():
    print("Loading sales data...")
    start_time = time.time()
    #time it takes to load the data
    try: 
        file_id = "1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
        url = f"https://drive.google.com/uc?id={file_id}&export=download"

        #loading directly from url
        df = pd.read_csv(url)
        df = normalize_column(df)
        df.fillna(0, inplace=True)

#check for req columns
        missing = [f for f in req_fields if f not in df.columns]
        if missing: 
            print(f"\nWarning: Missing required fields: {missing}.")
            print("Available columns: ", df.columns.tolist())
            sys.exit(1)

        print(f"\nLoaded {len(df)} rows and {len(df.columns)} columns.")
        print(f"Data loaded in {time.time() - start_time:.2f} seconds.")
        return df

    except Exception as e:
        print(f"\nError loading data: {str(e)}")
        sys.exit(1)

#displays first n rows of the dataframe
@handle_errors
def show_first_n_rows(df):
    max_rows = len(df)
    while True:
        choice = input(f"\nEnter the number of rows to display (1-{max_rows}), 'all', or Enter): ").strip().lower()
        if not choice:
            return None
        if choice == 'all':
            return df
        try:
            n = int(choice)
            if 1 <= n <= max_rows:
                return df.head(n)
            print(f"Please enter 1-{max_rows} or 'all'.")
        except ValueError:
            print("Invalid input. Please enter a number or 'all'.")

@handle_errors
#total slaes by region and order type
def total_sales_region_order_type(df):
    return pd.pivot_table(df, index = 'sales_region',
                            columns = 'order_type',
                            values = 'sales_price',
                            aggfunc = 'sum',
                            fill_value = 0)


#sales with percentage contributions, requirement 8
#used AI to help with this part, was unsure how to add the % in the pivot table
@handle_errors
def sales_region_product_percentages(df):
    pivot = pd.pivot_table(df,
                         index=['sales_region', 'product_category'],
                         values=['quantity', 'sales_price'],
                         aggfunc='sum')
    
    # Calculate percentages 
    region_totals = pivot.groupby('sales_region').transform('sum')
    
    pivot['quantity_pct'] = (pivot['quantity'] / region_totals['quantity'] * 100).round(2)
    pivot['sales_price_pct'] = (pivot['sales_price'] / region_totals['sales_price'] * 100).round(2)
    
    return pivot

#avg sales by region with avg sales by state and sale type
@handle_errors
def average_sales_region_state_sale_type(df):
    return pd.pivot_table(df, index='sales_region',
                            columns=['customer_state', 'order_type'],
                            values='sales_price',
                            aggfunc='mean',
                            fill_value=0)

#sales by customer type and order type by state
@handle_errors
def sales_customer_order_type_state(df):
    return pd.pivot_table(df, index='customer_state',
                            columns=['customer_type','order_type'],
                            values='sales_price',
                            aggfunc='sum',
                            fill_value=0)


#total quantity and price by region and product
@handle_errors
def total_sales_region_product(df):
    return pd.pivot_table(df, index=['sales_region','product_category'],
                            values=['quantity', 'sales_price'],
                            aggfunc='sum',
                            fill_value=0)

#total sales by customer type and order type
@handle_errors
def total_sales_customer_type(df):
    return pd.pivot_table(df, index=['customer_type','order_type'],
                            values=['quantity','sales_price'],
                            aggfunc='sum',
                            fill_value=0)

#max & min prices by category
@handle_errors
def max_min_sales_category(df):
    return pd.pivot_table(df, index='product_category',
                            values='sales_price',
                            aggfunc=['max','min'],
                            fill_value=0)


#unique employees by region
@handle_errors
def unique_employees_region(df):
    return pd.pivot_table(df, 
                      index='sales_region',
                      values='employee_name',
                      aggfunc=pd.Series.nunique,
                      fill_value=0)


#creating custom pivot table
@handle_errors
def create_custom_pivot(df):
    field_map = {
        'rows' : {
            1: 'employee_name',
            2: 'sales_region',
            3: 'product_category',
            4: 'customer_state',
            5: 'customer_type',
        }, 
        'columns' : {
            1: 'product_category',
            2: 'customer_state',
            3: 'customer_type',
            4: 'order_type',
        },
        'values' : {
            1: 'sales_price',
            2: 'quantity'
        },
        'agg' : {
            1: 'sum',
            2: 'mean',
            3: 'count',
            4: 'max',
            5: 'min',
            6: pd.Series.nunique
        }
    }

    def get_selection(category, required=True):
        print(f"\nSelect {category}:")
        options = field_map[category]
        for num, name in options.items():
            print(f"{num}. {name}")
        while True:
            choices = input(f"Enter numbers (comma-separated): ").strip()
            if not choices and not required:
                return None
            try:
                selected = [field_map[category][int(c)] 
                           for c in choices.split(',') if c.strip().isdigit()]
                if required and not selected:
                    raise ValueError
                return selected
            except (ValueError, KeyError):
                print("Invalid selection. Please try again.")
            
            #ask for user input
    try:
            print("\nCreating custom pivot table...")
            rows = get_selection('rows')
            cols = get_selection('columns', required=False)
            values = get_selection('values')
            agg_funcs = get_selection('agg')

            if not rows: 
                print("No rows selected. Exiting.")
                return None
            if not values:
                print("No values selected. Exiting.")
                return None

            return pd.pivot_table(df,
                                    index=rows,
                                    columns=cols if cols else None,
                                    values=values,
                                    aggfunc=agg_funcs if agg_funcs else 'mean',
                                    fill_value=0)
    except Exception as e:
        print(f"Error creating pivot table: {e}")
        return None

   
#exporting excel export, requirement 1
#used AI to figure out how to export files and how to handle exceptions
#AI made me install and import a library called openpyxl to export the files
def export_to_excel(result):
    if result is None:
        print("No data to export.")
        return False

    export_choice = input("Export to Excel? (y/n): ").strip().lower()
    if export_choice != 'y':    
        return False

    while True:
        filename = input("Enter filename (e.g., output.xlsx): ").strip()
        if not filename:
            print("Filename cannot be empty.")
            continue
    
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
        if not filename:
            print("Invalid filename. Please try again.")
            continue
        if not filename.lower().endswith('.xlsx'):
            filename = f"{filename}.xlsx"

        print (f"\n Will save as: {filename}")
        confirm = input(f"Is this correct? (y/n): ").strip().lower()
        if confirm == 'y':
            break
    
#performing the export
    try:
        result.to_excel(filename, engine='openpyxl')
        print(f"\n Successfully exported to {filename}")
        return True
    except PermissionError:
        print("\nError: could not save file.")
    
    except Exception as e:
            print(f"Export failed: {str(e)}")

    retry = input ("Retry? (y/n): ").strip().lower()
    if retry != 'y':
        return False


def main():
    df = load_data()
    
    while True:
        print("\n--- Sales Data Dashboard ---")
        for i, (label, _) in enumerate(menu_items, 1):
            print(f"{i}. {label}")
        
        try:
            choice = input("\nEnter choice (1-11): ").strip()
            if not choice:
                continue
            if choice == '11' or choice.lower() == 'exit':
                sys.exit("Exiting program.")
                
            choice_idx = int(choice) - 1
            _, func_name = menu_items[choice_idx]
            func = globals()[func_name]
            result = func(df)
            
            if result is not None:
                print(f"\n{' RESULT '.center(80, '=')}")
                print(result)
                export_to_excel(result)
                input ("\nPress Enter return to menu...")
        except (ValueError, IndexError):
            print(f"Invalid choice: {choice}. Please enter 1-11.")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()