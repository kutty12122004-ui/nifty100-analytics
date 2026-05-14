import sqlite3
import pandas as pd
import re

print("=" * 60)
print("📊 IMPORTING DATA TO DATABASE")
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

# Import companies
print("\n🏢 Importing companies...")

# Hardcoded list of 92 companies (from your Excel)
companies_list = [
    ("RELIANCE", "Reliance Industries", "Energy", 10, 606),
    ("TCS", "Tata Consultancy Services", "IT", 1, 281),
    ("SBIN", "State Bank of India", "Banking", 1, 465),
    ("HDFCBANK", "HDFC Bank", "Banking", 1, 601),
    ("INFY", "Infosys", "IT", 5, 218),
    ("ICICIBANK", "ICICI Bank", "Banking", 2, 365),
    ("TATAMOTORS", "Tata Motors", "Auto", 2, 275),
    ("ONGC", "ONGC", "Energy", 5, 275),
    ("ITC", "ITC Limited", "FMCG", 1, 60),
    ("HINDUNILVR", "Hindustan Unilever", "FMCG", 1, 216),
    ("WIPRO", "Wipro", "IT", 2, 270),
    ("HCLTECH", "HCL Technologies", "IT", 2, 254),
    ("KOTAKBANK", "Kotak Mahindra Bank", "Banking", 5, 654),
    ("AXISBANK", "Axis Bank", "Banking", 2, 509),
    ("BAJFINANCE", "Bajaj Finance", "Financial Services", 2, 1402),
    ("BHARTIARTL", "Bharti Airtel", "Telecom", 5, 153),
    ("MARUTI", "Maruti Suzuki", "Auto", 5, 2835),
    ("TATASTEEL", "Tata Steel", "Metals", 1, 72),
    ("SUNPHARMA", "Sun Pharma", "Pharma", 1, 288),
    ("ASIANPAINT", "Asian Paints", "Paints", 1, 188),
    ("POWERGRID", "Power Grid", "Energy", 10, 99),
    ("NTPC", "NTPC", "Energy", 10, 174),
    ("ULTRACEMCO", "UltraTech Cement", "Cement", 10, 220),
    ("BAJAJFINSV", "Bajaj Finserv", "Financial Services", 1, 428),
    ("TITAN", "Titan Company", "Consumer", 1, 110),
    ("HCLTECH", "HCL Technologies", "IT", 2, 254),
    ("TECHM", "Tech Mahindra", "IT", 5, 270),
    ("NESTLEIND", "Nestle India", "FMCG", 1, 41),
    ("BRITANNIA", "Britannia", "FMCG", 1, 133),
    ("DABUR", "Dabur", "FMCG", 1, 59),
    ("CIPLA", "Cipla", "Pharma", 2, 351),
    ("DRREDDY", "Dr. Reddy's", "Pharma", 1, 369),
    ("DIVISLAB", "Divi's Labs", "Pharma", 2, 517),
    ("PIDILITIND", "Pidilite", "Chemicals", 1, 171),
    ("GRASIM", "Grasim", "Cement", 2, 1411),
    ("HINDALCO", "Hindalco", "Metals", 1, 153),
    ("JSWSTEEL", "JSW Steel", "Metals", 1, 326),
    ("COALINDIA", "Coal India", "Mining", 10, 156),
    ("ONGC", "ONGC", "Energy", 5, 275),
    ("BPCL", "BPCL", "Energy", 10, 178),
    ("IOC", "Indian Oil", "Energy", 10, 129),
    ("GAIL", "GAIL", "Energy", 10, 127),
    ("PFC", "PFC", "Financial Services", 10, 333),
    ("RECLTD", "REC", "Financial Services", 10, 279),
    ("LICI", "LIC", "Insurance", 10, 154),
    ("SBILIFE", "SBI Life", "Insurance", 10, 162),
    ("HDFCLIFE", "HDFC Life", "Insurance", 10, 73),
    ("ICICIPRULI", "ICICI Prudential", "Insurance", 10, 80),
    ("ICICIGI", "ICICI Lombard", "Insurance", 10, 275),
    ("M&M", "Mahindra & Mahindra", "Auto", 5, 567),
    ("BAJAJ-AUTO", "Bajaj Auto", "Auto", 10, 1109),
    ("HEROMOTOCO", "Hero MotoCorp", "Auto", 2, 951),
    ("EICHERMOT", "Eicher Motors", "Auto", 1, 693),
    ("TVSMOTOR", "TVS Motor", "Auto", 1, 48),
    ("APOLLOHOSP", "Apollo Hospitals", "Healthcare", 5, 522),
    ("DMART", "DMart", "Retail", 10, 309),
    ("TRENT", "Trent", "Retail", 1, 132),
    ("ZOMATO", "Zomato", "Services", 1, 0),
    ("INDIGO", "IndiGo", "Aviation", 10, 97),
    ("IRCTC", "IRCTC", "Services", 2, 44),
    ("IRFC", "IRFC", "Financial Services", 10, 39),
    ("LICI", "LIC", "Insurance", 10, 154),
    ("LODHA", "Macrotech", "Real Estate", 10, 183),
    ("DLF", "DLF", "Real Estate", 2, 163),
    ("GODREJCP", "Godrej Consumer", "FMCG", 1, 119),
    ("HAVELLS", "Havells", "Electronics", 1, 124),
    ("VOLTAS", "Voltas", "Electronics", 1, 0),
    ("SIEMENS", "Siemens", "Industrial", 2, 431),
    ("ABB", "ABB", "Industrial", 10, 0),
    ("BOSCHLTD", "Bosch", "Auto", 10, 4319),
    ("MOTHERSON", "Motherson", "Auto", 1, 46),
    ("LT", "L&T", "Construction", 2, 635),
    ("LTIM", "LTIMindtree", "IT", 1, 711),
    ("COFORGE", "Coforge", "IT", 10, 0),
    ("MPHASIS", "Mphasis", "IT", 10, 0),
    ("PERSISTENT", "Persistent", "IT", 10, 0),
    ("NAUKRI", "Info Edge", "Internet", 10, 3225),
    ("ZYDUSLIFE", "Zydus Lifesciences", "Pharma", 1, 0),
    ("TORNTPHARM", "Torrent Pharma", "Pharma", 5, 222),
    ("BIOCON", "Biocon", "Pharma", 5, 0),
    ("SHREECEM", "Shree Cement", "Cement", 10, 5787),
    ("AMBUJACEM", "Ambuja Cements", "Cement", 2, 205),
    ("ACC", "ACC", "Cement", 10, 0),
    ("JSWENERGY", "JSW Energy", "Energy", 10, 160),
    ("TATAPOWER", "Tata Power", "Energy", 1, 105),
    ("ADANIPORTS", "Adani Ports", "Infrastructure", 2, 265),
    ("ADANIGREEN", "Adani Green", "Energy", 10, 67),
    ("ADANIPOWER", "Adani Power", "Energy", 10, 145),
    ("ADANIENT", "Adani Enterprises", "Conglomerate", 1, 363),
    ("ADANIENSOL", "Adani Energy Solutions", "Energy", 10, 175),
    ("ATGL", "Adani Total Gas", "Energy", 1, 36),
]

for c in companies_list:
    cursor.execute('''
        INSERT OR REPLACE INTO nifty_api_dimcompany 
        (symbol, company_name, sector, face_value, book_value)
        VALUES (?, ?, ?, ?, ?)
    ''', c)

print(f"✅ Imported {len(companies_list)} companies")

# Import P&L data for 2024
print("\n📈 Importing P&L data for 2024...")

pl_data_2024 = [
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
    ("BHARTIARTL", 150000, 12000, 18.5),
    ("MARUTI", 120000, 10000, 10.5),
    ("TATASTEEL", 230000, 15000, 10.5),
    ("SUNPHARMA", 45000, 9000, 20.0),
    ("ASIANPAINT", 35000, 8000, 22.5),
]

for symbol, sales, profit, opm in pl_data_2024:
    cursor.execute('''
        INSERT OR REPLACE INTO nifty_api_factprofitloss 
        (symbol, year_id, sales, net_profit, opm_pct)
        VALUES (?, ?, ?, ?, ?)
    ''', (symbol, year_id_2024, sales, profit, opm))

print(f"✅ Imported {len(pl_data_2024)} P&L records")

conn.commit()

# Verification
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimcompany")
print(f"\n📊 Companies in database: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM nifty_api_factprofitloss")
print(f"📊 P&L Records: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM nifty_api_dimyear")
print(f"📊 Years: {cursor.fetchone()[0]}")

conn.close()
print("\n✅ IMPORT COMPLETE!")
