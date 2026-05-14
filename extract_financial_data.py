import pandas as pd
import json

# Read the P&L data
df_pl = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=1)

# Create a dictionary to store financial data for each company
financial_data = {}

# Process each row
for _, row in df_pl.iterrows():
    symbol = str(row.get('company_id', '')).strip()
    if not symbol or symbol == 'nan':
        continue
    
    year = str(row.get('year', ''))
    # Only take 2024 data (not TTM)
    if '2024' in year and 'TTM' not in year and 'Mar 2024' in year:
        sales = row.get('sales', 0)
        net_profit = row.get('net_profit', 0)
        opm = row.get('opm_percentage', 0)
        
        if pd.notna(sales) and sales > 0:
            financial_data[symbol] = {
                'revenue_cr': float(sales),
                'net_profit_cr': float(net_profit) if pd.notna(net_profit) else 0,
                'opm_pct': float(opm) if pd.notna(opm) else 0
            }

print(f"Found financial data for {len(financial_data)} companies")
print("\nSample data:")
count = 0
for symbol, data in financial_data.items():
    print(f"  {symbol}: Revenue={data['revenue_cr']:,.0f} Cr, OPM={data['opm_pct']:.1f}%")
    count += 1
    if count >= 20:
        break

# Save to a JSON file for use in views.py
with open('financial_data.json', 'w') as f:
    json.dump(financial_data, f, indent=2)

print(f"\n✅ Saved financial data to financial_data.json")
