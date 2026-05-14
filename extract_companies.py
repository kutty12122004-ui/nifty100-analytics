import pandas as pd

# Read companies from Excel
df = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)

# Print each company as a dictionary entry
for _, row in df.iterrows():
    symbol = str(row.get('id', '')).strip()
    if symbol and symbol != 'nan' and symbol != '':
        name = str(row.get('company_name', ''))[:60].replace('"', '\\"')
        print(f'    {{"symbol": "{symbol}", "company_name": "{name}", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0}},')
