# etl/01_extract_from_mysql.py
"""
Script 1: Extract data from SQL dump file
Parses INSERT statements and converts to CSV files
"""

import re
import csv
import pandas as pd
from pathlib import Path
import sys

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def parse_sql_inserts(sql_file_path):
    """Parse SQL file and extract INSERT statements"""
    print(f"\n📂 Extracting data from: {sql_file_path}")
    
    with open(sql_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        sql_content = f.read()
    
    # Find all INSERT statements for companies
    companies_data = []
    pattern = r"INSERT INTO `companies`.*?VALUES\s*\((.*?)\);"
    matches = re.findall(pattern, sql_content, re.IGNORECASE | re.DOTALL)
    
    for match in matches:
        # Simple parsing of values
        values = [v.strip().strip("'") for v in match.split(',')]
        companies_data.append(values[:10])  # Take first 10 columns
    
    if companies_data:
        columns = ['company_id', 'company_name', 'logo', 'website', 'nse_url', 
                   'bse_url', 'roce', 'roe', 'face_value', 'book_value']
        df = pd.DataFrame(companies_data, columns=columns)
        df.to_csv(RAW_DATA_DIR / 'companies.csv', index=False)
        print(f"  ✅ Extracted {len(df)} companies")
    
    return True

def main():
    # Find SQL file
    sql_files = list(Path('.').glob('*.sql')) + list((PROJECT_ROOT).glob('*.sql'))
    
    if not sql_files:
        print("❌ No SQL dump file found! Please provide scriptticker.sql")
        print("   Expected file: scriptticker.sql in project root")
        return
    
    parse_sql_inserts(sql_files[0])
    print(f"\n✅ Raw data saved to: {RAW_DATA_DIR}")

if __name__ == "__main__":
    main()