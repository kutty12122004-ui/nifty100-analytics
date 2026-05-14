import sqlite3
import pandas as pd
import re

print("=" * 60)
print("📊 IMPORTING ALL 92 COMPANIES FROM EXCEL")
print("=" * 60)

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Drop and recreate tables
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimcompany")
cursor.execute("DROP TABLE IF EXISTS nifty_api_factprofitloss")
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimyear")

# Create companies table
cursor.execute('''
    CREATE TABLE nifty_api_dimcompany (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        face_value REAL,
        book_value REAL
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
        year_id INTEGER,
        sales REAL,
        net_profit REAL,
        opm_pct REAL
    )
''')

print("✅ Tables created")

# Import years
print("\n📅 Importing years...")
for year in range(2000, 2026):
    cursor.execute("INSERT OR IGNORE INTO nifty_api_dimyear (year_label) VALUES (?)", (str(year),))
print("✅ Years 2000-2025 imported")

# Get year_id for 2024
cursor.execute("SELECT year_id FROM nifty_api_dimyear WHERE year_label = '2024'")
year_id_2024 = cursor.fetchone()[0]

# ========== IMPORT ALL COMPANIES FROM EXCEL ==========
print("\n🏢 Reading companies from Excel...")

df_companies = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)
print(f"Found {len(df_companies)} companies in Excel")

# Sector mapping function
def get_sector(name):
    name_lower = name.lower()
    if any(w in name_lower for w in ['bank', 'hdfc', 'sbi', 'icici', 'axis', 'kotak', 'indusind', 'pnb', 'canara', 'baroda']):
        return 'Banking'
    elif any(w in name_lower for w in ['tech', 'tcs', 'infosys', 'wipro', 'hcl', 'techm', 'ltim', 'mindtree', 'coforge', 'mphasis']):
        return 'IT'
    elif any(w in name_lower for w in ['reliance', 'ongc', 'oil', 'gas', 'power', 'adani', 'ntpc', 'grid', 'energy', 'petroleum']):
        return 'Energy'
    elif any(w in name_lower for w in ['auto', 'motor', 'maruti', 'bajaj auto', 'hero', 'eicher', 'mahindra', 'tata motors']):
        return 'Auto'
    elif any(w in name_lower for w in ['pharma', 'sun', 'reddy', 'cipla', 'divis', 'biocon', 'torrent', 'labs']):
        return 'Pharma'
    elif any(w in name_lower for w in ['consumer', 'unilever', 'dabur', 'nestle', 'britannia', 'godrej', 'itc']):
        return 'FMCG'
    elif any(w in name_lower for w in ['finance', 'bajaj finance', 'bajaj finserv', 'lic', 'sbilife', 'insurance']):
        return 'Financial Services'
    elif any(w in name_lower for w in ['cement', 'ultra', 'ambuja', 'shree', 'acc']):
        return 'Cement'
    elif any(w in name_lower for w in ['steel', 'jsw', 'tata steel', 'hindalco', 'vedanta', 'coal']):
        return 'Metals & Mining'
    elif any(w in name_lower for w in ['paint', 'asian']):
        return 'Paints'
    elif any(w in name_lower for w in ['telecom', 'airtel']):
        return 'Telecom'
    else:
        return 'Other'

companies_imported = 0
for _, row in df_companies.iterrows():
    symbol = str(row.get('id', '')).strip()
    if not symbol or symbol == 'nan' or symbol == '':
        continue
    
    company_name = str(row.get('company_name', ''))[:200].replace('"', "'").replace('\n', ' ')
    sector = get_sector(company_name)
    
    face_value = float(row.get('face_value', 0)) if pd.notna(row.get('face_value')) else None
    book_value = float(row.get('book_value', 0)) if pd.notna(row.get('book_value')) else None
    
    cursor.execute('''
        INSERT OR REPLACE INTO nifty_api_dimcompany 
        (symbol, company_name, sector, face_value, book_value)
        VALUES (?, ?, ?, ?, ?)
    ''', (symbol, company_name, sector, face_value, book_value))
    companies_imported += 1

print(f"✅ Imported {companies_imported} companies")

# ========== IMPORT P&L DATA FROM EXCEL ==========
print("\n📈 Reading P&L data from Excel...")

df_pl = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=1)
print(f"Found {len(df_pl)} P&L records")

pl_imported = 0
for _, row in df_pl.iterrows():
    symbol = str(row.get('company_id', '')).strip()
    if not symbol or symbol == 'nan':
        continue
    
    year_str = str(row.get('year', ''))
    if 'TTM' in year_str or 'ttm' in year_str:
        continue
    
    year_match = re.search(r'\d{4}', year_str)
    if not year_match:
        continue
    
    year_num = int(year_match.group())
    
    # Get year_id
    cursor.execute("SELECT year_id FROM nifty_api_dimyear WHERE year_label = ?", (str(year_num),))
    year_result = cursor.fetchone()
    if not year_result:
        continue
    year_id = year_result[0]
    
    def safe_float(val):
        return float(val) if pd.notna(val) and val != 0 else 0
    
    sales = safe_float(row.get('sales', 0))
    net_profit = safe_float(row.get('net_profit', 0))
    opm = safe_float(row.get('opm_percentage', 0))
    
    if sales > 0 or net_profit != 0:
        cursor.execute('''
            INSERT OR REPLACE INTO nifty_api_factprofitloss 
            (symbol, year_id, sales, net_profit, opm_pct)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, year_id, sales, net_profit, opm))
        pl_imported += 1

print(f"✅ Imported {pl_imported} P&L records")

conn.commit()

# ========== VERIFICATION ==========
print("\n" + "=" * 60)
print("📊 VERIFICATION")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
print(f"   Companies: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
print(f"   P&L Records: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_dimyear")
print(f"   Years: {cursor.fetchone()[0]}")

# Show sample
print("\n📋 Sample companies:")
cursor.execute("SELECT symbol, company_name, sector FROM nifty_api_dimcompany LIMIT 15")
for row in cursor.fetchall():
    print(f"   - {row[0]}: {row[1][:40]} ({row[2]})")

conn.close()
print("\n✅ IMPORT COMPLETE!")
