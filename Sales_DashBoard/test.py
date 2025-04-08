import pandas as pd
import time
import sys
from functools import wraps

# ==================================================================
# Configuration Constants
# ==================================================================
REQUIRED_COLUMNS = {
    'sales_region', 'order_type', 'state', 'customer_type',
    'product_category', 'quantity', 'sale_price', 'employee_name'
}
MENU_ITEMS = [
    ("Show the first n rows of sales data", 'show_first_n_rows'),
    ("Total sales by region and order_type", 'total_sales_region_order_type'),
    ("Average sales by region with average sales by state and sale type", 'average_sales_region_state_sale_type'),
    ("Sales by customer type and order type by state", 'sales_customer_order_type_state'),
    ("Total sales quantity and price by region and product", 'total_sales_region_product'),
    ("Sales by region and product with percentages", 'sales_region_product_percentages'),
    ("Total sales quantity and price customer type", 'total_sales_customer_type'),
    ("Max and min sales price of sales by category", 'max_min_sales_category'),
    ("Number of unique employees by region", 'unique_employees_region'),
    ("Create a custom pivot table", 'create_custom_pivot'),
    ("Exit", 'exit_program')
]

# ==================================================================
# Error Handling Infrastructure
# ==================================================================
def handle_errors(required_columns=None):
    """
    Decorator factory for error handling and column validation
    - Checks for required columns before executing function
    - Handles pandas errors gracefully
    - Validates DataFrame existence
    """
    def decorator(func):
        @wraps(func)
        def wrapper(df, *args, **kwargs):
            # Validate DataFrame existence
            if df is None or df.empty:
                print("Error: No data loaded")
                return None
                
            # Check for required columns
            if required_columns:
                missing = required_columns - set(df.columns)
                if missing:
                    print(f"Error in {func.__name__}: Missing columns {missing}")
                    print("Available columns:", df.columns.tolist())
                    return None

            try:
                return func(df, *args, **kwargs)
            except KeyError as e:
                print(f"Column error in {func.__name__}: {str(e)} not found")
                print("Available columns:", df.columns.tolist())
                return None
            except Exception as e:
                print(f"Error in {func.__name__}: {str(e)}")
                return None
        return wrapper
    return decorator

# ==================================================================
# Core Data Loading Function (R1 Compliance)
# ==================================================================
def load_data():
    """Load and validate sales data from Google Drive with error handling"""
    print("\n[1/3] Connecting to Google Drive...")
    start_time = time.time()
    
    try:
        # Direct download URL for Google Drive CSV
        file_id = '1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA'
        url = f'https://drive.google.com/uc?id={file_id}&export=download'
        
        print("[2/3] Downloading data...")
        df = pd.read_csv(url)
        
        # Data cleaning and validation
        print("[3/3] Validating data...")
        df.fillna(0, inplace=True)
        
        # Column verification
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            print(f"Warning: Missing columns {missing} - some features may not work")
        
        # Success metrics
        print(f"\nSuccessfully loaded {len(df):,} rows")
        print(f"Time taken: {time.time()-start_time:.2f}s")
        print("Available columns:", df.columns.tolist())
        
        return df
        
    except Exception as e:
        print(f"\nFatal loading error: {str(e)}")
        sys.exit(1)

# ==================================================================
# Predefined Analytics (R3 Compliance)
# ==================================================================
@handle_errors(required_columns={'sales_region', 'order_type', 'sale_price'})
def total_sales_region_order_type(df):
    """
    R3.2: Total sales by region and order type
    - Rows: sales_region
    - Columns: order_type (Retail/Wholesale)
    - Values: sum(sale_price)
    """
    return pd.pivot_table(df,
                        index='sales_region',
                        columns='order_type',
                        values='sale_price',
                        aggfunc='sum',
                        fill_value=0)

@handle_errors(required_columns={'sales_region', 'state', 'order_type', 'sale_price'})
def average_sales_region_state_sale_type(df):
    """
    R3.3: Nested average sales breakdown
    - Main index: sales_region
    - Sub-columns: state × order_type
    - Values: mean(sale_price)
    """
    return pd.pivot_table(df,
                        index='sales_region',
                        columns=['state', 'order_type'],
                        values='sale_price',
                        aggfunc='mean',
                        fill_value=0)

@handle_errors(required_columns={'state', 'customer_type', 'order_type', 'sale_price'})
def sales_customer_order_type_state(df):
    """
    R3.4: Hierarchical sales breakdown
    - Index: state
    - Columns: customer_type × order_type
    - Values: sum(sale_price)
    """
    return pd.pivot_table(df,
                        index='state',
                        columns=['customer_type', 'order_type'],
                        values='sale_price',
                        aggfunc='sum',
                        fill_value=0)

# ==================================================================
# Additional Analytics with Percentage Calculation (R8)
# ==================================================================
@handle_errors(required_columns={'sales_region', 'product_category', 'quantity', 'sale_price'})
def sales_region_product_percentages(df):
    """
    R8: Regional product contribution with percentages
    - Calculates percentage of regional totals for each product
    - Returns DataFrame with original values and percentage columns
    """
    # Base pivot table
    pivot = pd.pivot_table(df,
                         index=['sales_region', 'product_category'],
                         values=['quantity', 'sale_price'],
                         aggfunc='sum')
    
    # Calculate regional totals
    region_totals = pivot.groupby('sales_region').transform('sum')
    
    # Add percentage columns
    pivot['quantity_pct'] = (pivot['quantity'] / region_totals['quantity'] * 100).round(2)
    pivot['sale_price_pct'] = (pivot['sale_price'] / region_totals['sale_price'] * 100).round(2)
    
    return pivot

# ==================================================================
# Interactive Pivot Table Generator (R4 Compliance)
# ==================================================================
@handle_errors()
def create_custom_pivot(df):
    """
    R4: Interactive pivot table builder
    - Guides user through pivot table creation
    - Handles multi-select inputs
    - Validates field selections
    """
    field_options = {
        'rows': {
            1: 'sales_region',
            2: 'employee_name',
            3: 'product_category',
            4: 'state',
            5: 'customer_type'
        },
        'cols': {
            1: 'order_type',
            2: 'customer_type',
            3: 'product_category',
            4: 'state'
        },
        'values': {
            1: 'quantity',
            2: 'sale_price'
        },
        'agg': {
            1: 'sum',
            2: 'mean',
            3: 'count',
            4: 'max',
            5: 'min',
            6: 'nunique'
        }
    }

    def validate_selection(category, required=True):
        """Helper function for validated multi-select input"""
        print(f"\nAvailable {category}:")
        for num, field in field_options[category].items():
            print(f"{num}: {field}")
            
        while True:
            choices = input(f"Choose {category} (comma-separated numbers): ").strip()
            if not choices and not required:
                return []
            try:
                selected = [field_options[category][int(c)] 
                           for c in choices.split(',') if c.strip().isdigit()]
                if required and not selected:
                    raise ValueError
                return selected
            except (ValueError, KeyError):
                print("Invalid selection. Please try again.")

    # Get user configuration
    print("\nBuilding Custom Pivot Table")
    rows = validate_selection('rows')
    cols = validate_selection('cols', required=False)
    values = validate_selection('values')
    agg_funcs = validate_selection('agg')

    # Create pivot table
    try:
        return pd.pivot_table(df,
                            index=rows,
                            columns=cols,
                            values=values,
                            aggfunc=agg_funcs,
                            fill_value=0)
    except Exception as e:
        print(f"Pivot creation failed: {str(e)}")
        return None

# ==================================================================
# Main Application Flow
# ==================================================================
def main():
    # Initialization
    df = load_data()
    
    # Main loop
    while True:
        print("\n=== Sales Analytics Dashboard ===")
        for idx, (label, _) in enumerate(MENU_ITEMS, 1):
            print(f"{idx}. {label}")
            
        try:
            choice = input("\nEnter option number: ").strip()
            if not choice:
                continue
                
            # Handle exit
            if choice == str(len(MENU_ITEMS)):
                print("Exiting program...")
                sys.exit()
                
            # Get selected function
            func_name = MENU_ITEMS[int(choice)-1][1]
            func = globals()[func_name]
            
            # Execute and display results
            result = func(df)
            if result is not None:
                print(f"\n{' RESULT '.center(80, '=')}")
                print(result)
                
                # Export prompt
                if input("\nExport to Excel? (y/n): ").lower() == 'y':
                    filename = input("Filename (e.g., analysis.xlsx): ").strip()
                    if not filename.endswith('.xlsx'):
                        filename += '.xlsx'
                    try:
                        result.to_excel(filename)
                        print(f"Saved to {filename}")
                    except Exception as e:
                        print(f"Export failed: {str(e)}")
                        
        except (ValueError, IndexError, KeyError):
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()