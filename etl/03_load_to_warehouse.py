# etl/03_load_to_warehouse.py
"""
Script 3: Load data to PostgreSQL
"""

import pandas as pd
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent
CLEAN_DATA_DIR = PROJECT_ROOT / 'data' / 'clean'

# Try to import PostgreSQL, but don't fail if not installed
try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️ psycopg2 not installed. PostgreSQL features disabled.")

def load_to_sqlite():
    """Fallback to SQLite if PostgreSQL not available"""
    import sqlite3
    
    print("\n💾 Loading data to SQLite...")
    sqlite_path = PROJECT_ROOT / 'db.sqlite3'
    conn = sqlite3.connect(sqlite_path)
    
    # Load companies
    companies_file = CLEAN_DATA_DIR / 'companies_clean.csv'
    if companies_file.exists():
        df = pd.read_csv(companies_file)
        if 'company_id' in df.columns:
            df = df.rename(columns={'company_id': 'symbol'})
        df.to_sql('nifty_api_dimcompany', conn, if_exists='replace', index=False)
        print(f"  ✅ Loaded {len(df)} companies to SQLite")
    
    # Load profit & loss
    pl_file = CLEAN_DATA_DIR / 'profitandloss_clean.csv'
    if pl_file.exists():
        df = pd.read_csv(pl_file)
        df.to_sql('nifty_api_factprofitloss', conn, if_exists='replace', index=False)
        print(f"  ✅ Loaded {len(df)} profit & loss records to SQLite")
    
    # Load balance sheet
    bs_file = CLEAN_DATA_DIR / 'balancesheet_clean.csv'
    if bs_file.exists():
        df = pd.read_csv(bs_file)
        df.to_sql('nifty_api_factbalancesheet', conn, if_exists='replace', index=False)
        print(f"  ✅ Loaded {len(df)} balance sheet records to SQLite")
    
    conn.close()
    print(f"\n✅ Data loaded to SQLite: {sqlite_path}")

def main():
    print("\n" + "="*60)
    print("📤 LOADING TO DATA WAREHOUSE")
    print("="*60)
    
    # Check if clean data exists
    if not CLEAN_DATA_DIR.exists():
        print("❌ Clean data directory not found!")
        print("   Please run 02_clean_and_transform.py first")
        return
    
    # Load to SQLite (always works)
    load_to_sqlite()
    
    print("\n✅ Loading complete!")

if __name__ == "__main__":
    main()