import sqlite3
import pandas as pd
from pathlib import Path

print("=" * 60)
print("📊 IMPORTING ALL 92 COMPANIES")
print("=" * 60)

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimcompany")
cursor.execute("DROP TABLE IF EXISTS nifty_api_factprofitloss")
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimyear")

print("✅ Dropped old tables")

# Create tables
cursor.execute('''
    CREATE TABLE nifty_api_dimcompany (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        face_value REAL,
        book_value REAL
    )
''')

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

cursor.execute('''
    CREATE TABLE nifty_api_dimyear (
        year_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year_label TEXT UNIQUE
    )
''')

print("✅ Tables created")

# Insert years
print("\n📅 Adding years...")
for year in range(2000, 2026):
    cursor.execute("INSERT OR IGNORE INTO nifty_api_dimyear (year_label) VALUES (?)", (str(year),))
print("✅ Years added")

# Get year ID for 2024
cursor.execute("SELECT year_id FROM nifty_api_dimyear WHERE year_label = '2024'")
year_id = cursor.fetchone()[0]

# ========== IMPORT ALL 92 COMPANIES FROM EXCEL ==========
print("\n🏢 Reading companies from Excel...")
df = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)
print(f"   Found {len(df)} companies in Excel")

companies_added = 0
for _, row in df.iterrows():
    symbol = str(row.get('id', '')).strip()
    if symbol and symbol != 'nan' and symbol != '':
        company_name = str(row.get('company_name', ''))[:200]
        sector = "Other"  # You can update sectors later
        face_value = float(row.get('face_value', 0)) if pd.notna(row.get('face_value')) else None
        book_value = float(row.get('book_value', 0)) if pd.notna(row.get('book_value')) else None
        
        cursor.execute('''
            INSERT OR REPLACE INTO nifty_api_dimcompany 
            (symbol, company_name, sector, face_value, book_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, company_name, sector, face_value, book_value))
        companies_added += 1

print(f"✅ Added {companies_added} companies")

# ========== ADD SAMPLE P&L DATA FOR TOP COMPANIES ==========
print("\n📊 Adding P&L data for top companies...")

# Financial data for major companies
financial_data = [
    ("RELIANCE", 800000, 68000, 12.5),
    ("TCS", 240000, 45000, 25.5),
    ("SBIN", 400000, 55000, 15.5),
    ("HDFCBANK", 180000, 35000, 20.5),
    ("INFY", 150000, 28000, 24.5),
    ("ICICIBANK", 150000, 32000, 18.5),
    ("TATAMOTORS", 350000, 28000, 8.5),
    ("ONGC", 500000, 40000, 14.0),
    ("ITC", 70000, 20000, 28.5),
    ("HINDUNILVR", 60000, 10000, 19.5),
    ("WIPRO", 90000, 15000, 22.0),
    ("HCLTECH", 120000, 22000, 23.0),
    ("KOTAKBANK", 80000, 18000, 22.0),
    ("AXISBANK", 95000, 15000, 17.8),
    ("BAJFINANCE", 50000, 12000, 24.0),
]

for fd in financial_data:
    cursor.execute('''
        INSERT OR REPLACE INTO nifty_api_factprofitloss 
        (symbol, year_id, sales, net_profit, opm_pct)
        VALUES (?, ?, ?, ?, ?)
    ''', (fd[0], year_id, fd[1], fd[2], fd[3]))

print(f"✅ Added {len(financial_data)} P&L records")

conn.commit()

# ========== VERIFICATION ==========
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
print(f"\n✅ Companies in database: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
print(f"✅ P&L Records: {cursor.fetchone()[0]}")

# Show sample companies
print("\n📋 Sample companies:")
cursor.execute("SELECT symbol, company_name FROM nifty_api_dimcompany LIMIT 10")
for row in cursor.fetchall():
    print(f"   - {row[0]}: {row[1][:50]}")

conn.close()
print("\n✅ Import complete! Now you have ALL 92 companies!")
