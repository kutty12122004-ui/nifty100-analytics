import sqlite3
import pandas as pd
from pathlib import Path

print("=" * 60)
print("📊 IMPORTING NIFTY 100 DATA")
print("=" * 60)

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Import companies
companies_file = Path('data/clean/companies_clean.csv')
if companies_file.exists():
    df = pd.read_csv(companies_file)
    print(f"✅ Found {len(df)} companies")
    
    # Clear and insert
    cursor.execute("DELETE FROM nifty_api_dimcompany")
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO nifty_api_dimcompany 
            (symbol, company_name, sector, face_value, book_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row.get('company_id', row.get('symbol', '')),
            row.get('company_name', ''),
            row.get('sector', ''),
            row.get('face_value', 0),
            row.get('book_value', 0)
        ))
    conn.commit()
    print(f"✅ Imported {len(df)} companies")

# Import profit & loss
pl_file = Path('data/clean/profitandloss_clean.csv')
if pl_file.exists():
    df = pd.read_csv(pl_file)
    print(f"✅ Found {len(df)} P&L records")
    
    cursor.execute("DELETE FROM nifty_api_factprofitloss")
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO nifty_api_factprofitloss 
            (symbol, year, sales, net_profit, opm_pct)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row.get('company_id', ''),
            row.get('year', ''),
            float(row.get('sales', 0)) if pd.notna(row.get('sales')) else 0,
            float(row.get('net_profit', 0)) if pd.notna(row.get('net_profit')) else 0,
            float(row.get('opm_percentage', 0)) if pd.notna(row.get('opm_percentage')) else 0
        ))
    conn.commit()
    print(f"✅ Imported {len(df)} P&L records")

# Verify
cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss WHERE sales > 0")
sales_count = cursor.fetchone()[0]
print(f"\n📊 Records with sales data: {sales_count}")

cursor.execute("SELECT SUM(sales) FROM nifty_api_factprofitloss")
total_sales = cursor.fetchone()[0] or 0
print(f"💰 Total Revenue: {total_sales:,.0f} Cr")

conn.close()
print("\n✅ Import complete!")
