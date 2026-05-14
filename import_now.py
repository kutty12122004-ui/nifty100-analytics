import sqlite3
import pandas as pd

print("=" * 60)
print("📊 IMPORTING DATA TO DATABASE")
print("=" * 60)

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Drop and recreate tables with correct schema
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimcompany")
cursor.execute("DROP TABLE IF EXISTS nifty_api_factprofitloss")

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

# Create P&L table with year_id (not year)
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

# Create years table
cursor.execute("DROP TABLE IF EXISTS nifty_api_dimyear")
cursor.execute('''
    CREATE TABLE nifty_api_dimyear (
        year_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year_label TEXT UNIQUE
    )
''')

print("✅ Tables created")

# Insert years
print("\n📅 Inserting years...")
for year in range(2000, 2026):
    cursor.execute("INSERT OR IGNORE INTO nifty_api_dimyear (year_label) VALUES (?)", (str(year),))
print("✅ Years inserted")

# Get year_id for 2024
cursor.execute("SELECT year_id FROM nifty_api_dimyear WHERE year_label = '2024'")
year_id_2024 = cursor.fetchone()[0]

# Read companies from Excel
print("\n📖 Reading companies from Excel...")
df = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)

# Insert companies
count = 0
for _, row in df.iterrows():
    symbol = str(row.get('id', '')).strip()
    if symbol and symbol != 'nan':
        name = str(row.get('company_name', ''))[:100]
        face_value = float(row.get('face_value', 0)) if pd.notna(row.get('face_value')) else None
        book_value = float(row.get('book_value', 0)) if pd.notna(row.get('book_value')) else None
        
        cursor.execute('''
            INSERT OR REPLACE INTO nifty_api_dimcompany 
            (symbol, company_name, sector, face_value, book_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, 'Other', face_value, book_value))
        count += 1

print(f"✅ Imported {count} companies")

# Insert financial data
print("\n💰 Inserting financial data...")

financial_data = [
    ("RELIANCE", year_id_2024, 800000, 68000, 12.5),
    ("TCS", year_id_2024, 240000, 45000, 25.5),
    ("SBIN", year_id_2024, 400000, 55000, 15.5),
    ("HDFCBANK", year_id_2024, 180000, 35000, 20.5),
    ("INFY", year_id_2024, 150000, 28000, 24.5),
    ("ICICIBANK", year_id_2024, 150000, 32000, 18.5),
    ("TATAMOTORS", year_id_2024, 350000, 28000, 8.5),
    ("ONGC", year_id_2024, 500000, 40000, 14.0),
    ("ITC", year_id_2024, 70000, 20000, 28.5),
    ("HINDUNILVR", year_id_2024, 60000, 10000, 19.5),
    ("WIPRO", year_id_2024, 90000, 15000, 22.0),
    ("HCLTECH", year_id_2024, 120000, 22000, 23.0),
    ("KOTAKBANK", year_id_2024, 80000, 18000, 22.0),
    ("AXISBANK", year_id_2024, 95000, 15000, 17.8),
    ("BAJFINANCE", year_id_2024, 50000, 12000, 24.0),
]

for data in financial_data:
    cursor.execute('''
        INSERT OR REPLACE INTO nifty_api_factprofitloss 
        (symbol, year_id, sales, net_profit, opm_pct)
        VALUES (?, ?, ?, ?, ?)
    ''', data)

print(f"✅ Inserted {len(financial_data)} financial records")

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
print(f"\n📊 Total companies: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
print(f"📊 Financial records: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_dimyear")
print(f"📊 Years: {cursor.fetchone()[0]}")

# Sample
print("\n📋 Sample companies:")
cursor.execute("SELECT symbol, company_name FROM nifty_api_dimcompany LIMIT 10")
for row in cursor.fetchall():
    print(f"   - {row[0]}: {row[1][:40]}")

conn.close()
print("\n✅ IMPORT COMPLETE!")
