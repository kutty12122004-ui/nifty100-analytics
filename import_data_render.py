import sqlite3
import pandas as pd
from pathlib import Path
import os

print("=" * 60)
print("📊 Importing Nifty 100 Data to Database")
print("=" * 60)

# Connect to SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check if clean data exists
clean_dir = Path('data/clean')

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nifty_api_dimcompany (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        face_value REAL,
        book_value REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS nifty_api_factprofitloss (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        year TEXT,
        sales REAL,
        net_profit REAL,
        opm_pct REAL
    )
''')

# Import companies
companies_file = clean_dir / 'companies_clean.csv'
if companies_file.exists():
    df = pd.read_csv(companies_file)
    print(f"📁 Found {len(df)} companies")
    
    if 'company_id' in df.columns:
        df = df.rename(columns={'company_id': 'symbol'})
    
    # Clear existing
    cursor.execute("DELETE FROM nifty_api_dimcompany")
    
    # Insert companies
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT OR REPLACE INTO nifty_api_dimcompany 
            (symbol, company_name, sector, face_value, book_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row.get('symbol', ''),
            row.get('company_name', ''),
            row.get('sector', ''),
            row.get('face_value', 0),
            row.get('book_value', 0)
        ))
    
    conn.commit()
    print(f"✅ Imported {len(df)} companies")
else:
    print(f"❌ Companies file not found: {companies_file}")

# Import profit & loss
pl_file = clean_dir / 'profitandloss_clean.csv'
if pl_file.exists():
    df = pd.read_csv(pl_file)
    print(f"📁 Found {len(df)} profit & loss records")
    
    # Clear existing
    cursor.execute("DELETE FROM nifty_api_factprofitloss")
    
    # Insert records
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO nifty_api_factprofitloss 
            (symbol, year, sales, net_profit, opm_pct)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row.get('company_id', ''),
            row.get('year', ''),
            row.get('sales', 0),
            row.get('net_profit', 0),
            row.get('opm_percentage', 0)
        ))
    
    conn.commit()
    print(f"✅ Imported {len(df)} profit & loss records")
else:
    print(f"⚠️ Profit & Loss file not found: {pl_file}")

# Verify
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
companies_count = cursor.fetchone()[0]
print(f"\n🏢 Companies in database: {companies_count}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
pl_count = cursor.fetchone()[0]
print(f"📈 Profit & Loss records: {pl_count}")

conn.close()
print("\n" + "=" * 60)
print("✅ Data import complete!")
print("=" * 60)
