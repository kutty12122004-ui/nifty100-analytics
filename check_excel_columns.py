import pandas as pd

print("Checking Profit & Loss Excel file...")
df_pl = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', skiprows=2)
print(f"Columns in P&L file: {list(df_pl.columns)}")
print(f"First row of data: {df_pl.iloc[0].to_dict()}")
print(f"\nTotal rows: {len(df_pl)}")

print("\n" + "="*50)
print("Checking Balance Sheet Excel file...")
try:
    df_bs = pd.read_excel('balancesheet.xlsx', sheet_name='Balance Sheet', skiprows=2)
    print(f"Columns in Balance Sheet: {list(df_bs.columns)}")
    print(f"First row of data: {df_bs.iloc[0].to_dict()}")
    print(f"Total rows: {len(df_bs)}")
except Exception as e:
    print(f"Error reading balance sheet: {e}")