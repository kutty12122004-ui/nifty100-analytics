# import_real_data.py
import sqlite3
import pandas as pd
from pathlib import Path

print("=" * 60)
print("📊 Importing Real Nifty 100 ETL Data")
print("=" * 60)

# Connect to SQLite
conn = sqlite3.connect('db.sqlite3')

# Check for clean data
clean_dir = Path('data/clean')
if not clean_dir.exists():
    print(f"❌ Clean data directory not found: {clean_dir}")
    print("Please run your ETL pipeline first!")
    exit(1)

# Import companies
companies_file = clean_dir / 'companies_clean.csv'
if companies_file.exists():
    df = pd.read_csv(companies_file)
    print(f"📁 Found {len(df)} companies")
    
    # Rename columns
    if 'company_id' in df.columns:
        df = df.rename(columns={'company_id': 'symbol'})
    
    # Select relevant columns
    columns_needed = ['symbol', 'company_name', 'sector', 'website', 'face_value', 'book_value']
    existing_cols = [col for col in columns_needed if col in df.columns]
    df = df[existing_cols]
    
    df.to_sql('nifty_api_dimcompany', conn, if_exists='replace', index=False)
    print(f"✅ Imported {len(df)} companies to database")
else:
    print(f"❌ Companies file not found: {companies_file}")

# Import profit & loss
pl_file = clean_dir / 'profitandloss_clean.csv'
if pl_file.exists():
    df = pd.read_csv(pl_file)
    print(f"📁 Found {len(df)} profit & loss records")
    df.to_sql('nifty_api_factprofitloss', conn, if_exists='replace', index=False)
    print(f"✅ Imported {len(df)} profit & loss records")
else:
    print(f"⚠️ Profit & Loss file not found, using sample data")

# Import balance sheet
bs_file = clean_dir / 'balancesheet_clean.csv'
if bs_file.exists():
    df = pd.read_csv(bs_file)
    print(f"📁 Found {len(df)} balance sheet records")
    df.to_sql('nifty_api_factbalancesheet', conn, if_exists='replace', index=False)
    print(f"✅ Imported {len(df)} balance sheet records")
else:
    print(f"⚠️ Balance Sheet file not found, using sample data")

# Verify import
print("\n" + "=" * 60)
print("📊 Database Verification")
print("=" * 60)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
companies_count = cursor.fetchone()[0]
print(f"🏢 Companies in database: {companies_count}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
pl_count = cursor.fetchone()[0]
print(f"📈 Profit & Loss records: {pl_count}")

cursor.execute("SELECT COUNT(*) FROM nifty_api_factbalancesheet")
bs_count = cursor.fetchone()[0]
print(f"📊 Balance Sheet records: {bs_count}")

# Show sample companies
if companies_count > 0:
    print("\n📋 Sample companies in database:")
    cursor.execute("SELECT symbol, company_name FROM nifty_api_dimcompany LIMIT 10")
    samples = cursor.fetchall()
    for symbol, name in samples:
        print(f"   • {symbol}: {name[:50]}")

conn.close()

print("\n" + "=" * 60)
print("✅ Data import complete!")
print("=" * 60)
print("\n🚀 Restart your server and test the API:")
print("   python manage.py runserver")
print("\n📡 Test endpoints:")
print("   http://127.0.0.1:8000/api/companies/")
print("   http://127.0.0.1:8000/api/companies/TCS/")