import sqlite3
import pandas as pd
import re
import os

print("=" * 60)
print("📊 IMPORTING DATA TO DATABASE")
print("=" * 60)

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS nifty_api_dimyear (
        year_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year_label TEXT UNIQUE
    )
''')

print("✅ Tables created")

# Import companies
print("\n🏢 Importing companies...")
df_companies = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)
count = 0
for _, row in df_companies.iterrows():
    symbol = str(row.get('id', '')).strip()
    if symbol and symbol != 'nan':
        name = str(row.get('company_name', ''))[:200]
        cursor.execute('''
            INSERT OR REPLACE INTO nifty_api_dimcompany (symbol, company_name, sector, face_value, book_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, 'Other', None, None))
        count += 1
print(f"✅ Imported {count} companies")

# Import years
print("\n📅 Importing years...")
for year in range(2000, 2026):
    cursor.execute("INSERT OR IGNORE INTO nifty_api_dimyear (year_label) VALUES (?)", (str(year),))
print("✅ Years imported")

# Import P&L data (sample for top companies)
print("\n📈 Importing sample P&L data...")
sample_data = [
    ("RELIANCE", "Mar 2024", 800000, 68000, 12.5),
    ("TCS", "Mar 2024", 240000, 45000, 25.5),
    ("SBIN", "Mar 2024", 400000, 55000, 15.5),
    ("HDFCBANK", "Mar 2024", 180000, 35000, 20.5),
    ("INFY", "Mar 2024", 150000, 28000, 24.5),
    ("ICICIBANK", "Mar 2024", 150000, 32000, 18.5),
    ("TATAMOTORS", "Mar 2024", 350000, 28000, 8.5),
    ("ONGC", "Mar 2024", 500000, 40000, 14.0),
    ("ITC", "Mar 2024", 70000, 20000, 28.5),
    ("HINDUNILVR", "Mar 2024", 60000, 10000, 19.5),
]

for data in sample_data:
    cursor.execute('''
        INSERT OR REPLACE INTO nifty_api_factprofitloss (symbol, year, sales, net_profit, opm_pct)
        VALUES (?, ?, ?, ?, ?)
    ''', data)
print(f"✅ Imported {len(sample_data)} P&L records")

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
print(f"\n📊 Companies in database: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
print(f"📊 P&L Records: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimyear")
print(f"📊 Years: {cursor.fetchone()[0]}")

conn.close()
print("\n✅ IMPORT COMPLETE!")
