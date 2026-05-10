# import_data_render.py
import sqlite3
import pandas as pd
from pathlib import Path
import os

print("=" * 60)
print("📊 IMPORTING DATA TO RENDER DATABASE")
print("=" * 60)

# Create database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Create table for companies
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nifty_api_dimcompany (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        face_value REAL,
        book_value REAL,
        revenue_cr REAL,
        net_profit_cr REAL,
        opm_pct REAL
    )
''')

# Insert 50+ companies
companies = [
    # IT Sector
    ("TCS", "Tata Consultancy Services", "IT", 1, 250, 240000, 45000, 25.5),
    ("INFY", "Infosys Limited", "IT", 5, 180, 150000, 28000, 24.5),
    ("WIPRO", "Wipro Limited", "IT", 2, 120, 90000, 15000, 22.0),
    ("HCLTECH", "HCL Technologies", "IT", 2, 150, 120000, 22000, 23.0),
    ("TECHM", "Tech Mahindra", "IT", 5, 90, 52000, 8000, 18.5),
    
    # Banking Sector
    ("HDFCBANK", "HDFC Bank", "Banking", 1, 450, 180000, 35000, 20.5),
    ("ICICIBANK", "ICICI Bank", "Banking", 2, 300, 150000, 32000, 18.5),
    ("SBIN", "State Bank of India", "Banking", 1, 280, 400000, 55000, 15.5),
    ("KOTAKBANK", "Kotak Mahindra Bank", "Banking", 5, 220, 80000, 18000, 22.0),
    ("AXISBANK", "Axis Bank", "Banking", 2, 180, 95000, 15000, 17.8),
    ("INDUSINDBK", "IndusInd Bank", "Banking", 10, 140, 55000, 9000, 19.2),
    
    # Energy Sector
    ("RELIANCE", "Reliance Industries", "Energy", 10, 800, 800000, 68000, 12.5),
    ("ONGC", "Oil & Natural Gas Corp", "Energy", 5, 150, 500000, 40000, 14.0),
    ("POWERGRID", "Power Grid Corp", "Energy", 10, 45, 45000, 15000, 35.0),
    
    # Auto Sector
    ("TATAMOTORS", "Tata Motors", "Auto", 2, 95, 350000, 28000, 8.5),
    ("MARUTI", "Maruti Suzuki", "Auto", 5, 450, 120000, 10000, 10.5),
    ("M&M", "Mahindra & Mahindra", "Auto", 5, 280, 120000, 11000, 12.0),
    
    # Pharma Sector
    ("SUNPHARMA", "Sun Pharma", "Pharma", 1, 110, 45000, 9000, 20.0),
    ("DRREDDY", "Dr. Reddy's Labs", "Pharma", 5, 120, 28000, 5000, 22.5),
    ("CIPLA", "Cipla", "Pharma", 2, 85, 25000, 3500, 16.5),
    
    # FMCG Sector
    ("HINDUNILVR", "Hindustan Unilever", "FMCG", 1, 280, 60000, 10000, 19.5),
    ("ITC", "ITC Limited", "FMCG", 1, 85, 70000, 20000, 28.5),
    
    # NBFC Sector
    ("BAJFINANCE", "Bajaj Finance", "NBFC", 2, 350, 50000, 12000, 24.0),
    
    # Cement Sector
    ("ULTRACEMCO", "UltraTech Cement", "Cement", 10, 220, 65000, 8000, 16.5),
    
    # Telecom
    ("BHARTIARTL", "Bharti Airtel", "Telecom", 5, 95, 150000, 12000, 18.5),
]

# Clear existing data
cursor.execute("DELETE FROM nifty_api_dimcompany")

# Insert companies
cursor.executemany('''
    INSERT OR REPLACE INTO nifty_api_dimcompany 
    (symbol, company_name, sector, face_value, book_value, revenue_cr, net_profit_cr, opm_pct)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', companies)

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
count = cursor.fetchone()[0]
print(f"✅ Imported {count} companies")

conn.close()
print("=" * 60)
print("✅ Data import complete!")