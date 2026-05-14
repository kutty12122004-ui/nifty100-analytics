import sqlite3
import pandas as pd
import re
from pathlib import Path

print("=" * 60)
print("📊 DIRECT IMPORT TO SQLITE")
print("=" * 60)

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# ========== DROP AND CREATE TABLES ==========
print("\n📋 Creating tables...")

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimcompany")
cursor.execute("DROP TABLE IF EXISTS nifty_api_factprofitloss")
cursor.execute("DROP TABLE IF EXISTS nifty_api_factbalancesheet")
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimyear")

# Create companies table
cursor.execute('''
    CREATE TABLE nifty_api_dimcompany (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        face_value REAL,
        book_value REAL,
        website TEXT,
        nse_url TEXT,
        bse_url TEXT
    )
''')

# Create years table
cursor.execute('''
    CREATE TABLE nifty_api_dimyear (
        year_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year_label TEXT UNIQUE
    )
''')

# Create P&L table
cursor.execute('''
    CREATE TABLE nifty_api_factprofitloss (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        year TEXT,
        sales REAL,
        net_profit REAL,
        opm_pct REAL,
        eps REAL
    )
''')

# Create Balance Sheet table
cursor.execute('''
    CREATE TABLE nifty_api_factbalancesheet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        year TEXT,
        total_assets REAL,
        borrowings REAL,
        equity_capital REAL,
        reserves REAL
    )
''')

print("   ✅ Tables created")

# ========== IMPORT COMPANIES ==========
print("\n🏢 Importing Companies...")
companies_file = Path('companies.xlsx')
if companies_file.exists():
    df = pd.read_excel(companies_file, sheet_name='Companies', header=1)
    print(f"   Found {len(df)} companies")
    
    for _, row in df.iterrows():
        symbol = str(row.get('id', '')).strip()
        if symbol and symbol != 'nan':
            cursor.execute('''
                INSERT INTO nifty_api_dimcompany 
                (symbol, company_name, sector, face_value, book_value, website, nse_url, bse_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                str(row.get('company_name', ''))[:200],
                'Other',
                float(row.get('face_value', 0)) if pd.notna(row.get('face_value')) else None,
                float(row.get('book_value', 0)) if pd.notna(row.get('book_value')) else None,
                str(row.get('website', '')) if pd.notna(row.get('website')) else None,
                str(row.get('nse_profile', '')) if pd.notna(row.get('nse_profile')) else None,
                str(row.get('bse_profile', '')) if pd.notna(row.get('bse_profile')) else None,
            ))
    
    conn.commit()
    print(f"   ✅ Imported {len(df)} companies")
else:
    print(f"   ❌ companies.xlsx not found!")

# ========== IMPORT YEARS ==========
print("\n📅 Importing Years...")
for year in range(2000, 2026):
    cursor.execute("INSERT INTO nifty_api_dimyear (year_label) VALUES (?)", (str(year),))
conn.commit()
print(f"   ✅ Created years 2000-2025")

# ========== IMPORT PROFIT & LOSS ==========
print("\n📈 Importing Profit & Loss...")
pl_file = Path('profitandloss.xlsx')
if pl_file.exists():
    df = pd.read_excel(pl_file, sheet_name='Profit & Loss', header=1)
    print(f"   Found {len(df)} records")
    
    pl_count = 0
    for _, row in df.iterrows():
        symbol = str(row.get('company_id', '')).strip()
        if not symbol or symbol == 'nan':
            continue
        
        year_str = str(row.get('year', ''))
        year_match = re.search(r'\d{4}', year_str)
        if not year_match:
            continue
        
        year = year_match.group()
        
        def safe_float(val):
            return float(val) if pd.notna(val) else 0
        
        try:
            cursor.execute('''
                INSERT INTO nifty_api_factprofitloss 
                (symbol, year, sales, net_profit, opm_pct, eps)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                symbol, year,
                safe_float(row.get('sales', 0)),
                safe_float(row.get('net_profit', 0)),
                safe_float(row.get('opm_percentage', 0)),
                safe_float(row.get('eps', 0))
            ))
            pl_count += 1
        except Exception as e:
            pass
    
    conn.commit()
    print(f"   ✅ Imported {pl_count} P&L records")
else:
    print(f"   ❌ profitandloss.xlsx not found!")

# ========== IMPORT BALANCE SHEET ==========
print("\n📊 Importing Balance Sheet...")
bs_file = Path('balancesheet.xlsx')
if bs_file.exists():
    df = pd.read_excel(bs_file, sheet_name='Balance Sheet', header=1)
    print(f"   Found {len(df)} records")
    
    bs_count = 0
    for _, row in df.iterrows():
        symbol = str(row.get('company_id', '')).strip()
        if not symbol or symbol == 'nan':
            continue
        
        year_str = str(row.get('year', ''))
        year_match = re.search(r'\d{4}', year_str)
        if not year_match:
            continue
        
        year = year_match.group()
        
        def safe_float(val):
            return float(val) if pd.notna(val) else 0
        
        try:
            cursor.execute('''
                INSERT INTO nifty_api_factbalancesheet 
                (symbol, year, total_assets, borrowings, equity_capital, reserves)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                symbol, year,
                safe_float(row.get('total_assets', 0)),
                safe_float(row.get('borrowings', 0)),
                safe_float(row.get('equity_capital', 0)),
                safe_float(row.get('reserves', 0))
            ))
            bs_count += 1
        except Exception as e:
            pass
    
    conn.commit()
    print(f"   ✅ Imported {bs_count} Balance Sheet records")
else:
    print(f"   ❌ balancesheet.xlsx not found!")

# ========== VERIFICATION ==========
print("\n" + "=" * 60)
print("📊 VERIFICATION")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
print(f"   Companies: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
print(f"   P&L Records: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factbalancesheet")
print(f"   Balance Sheet Records: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_dimyear")
print(f"   Years: {cursor.fetchone()[0]}")

# Show sample
print("\n📋 Sample companies:")
cursor.execute("SELECT symbol, company_name FROM nifty_api_dimcompany LIMIT 10")
for row in cursor.fetchall():
    print(f"   - {row[0]}: {row[1][:50]}")

conn.close()
print("\n✅ Import complete! Your database now has real data.")
