# etl/02_clean_and_transform.py (UPDATED)
"""
Script 2: Clean and transform raw data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
CLEAN_DATA_DIR = PROJECT_ROOT / 'data' / 'clean'
CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)

def clean_companies():
    """Clean companies data"""
    print("\n🏢 Cleaning companies data...")
    
    raw_file = RAW_DATA_DIR / 'companies.csv'
    if not raw_file.exists():
        print("  ⚠️ companies.csv not found - creating sample data")
        return create_sample_companies()
    
    df = pd.read_csv(raw_file)
    print(f"  📁 Loaded {len(df)} raw records")
    print(f"  📋 Columns: {list(df.columns)}")
    
    # Check for column name variations
    company_id_col = None
    for col in ['company_id', 'id', 'symbol']:
        if col in df.columns:
            company_id_col = col
            break
    
    if company_id_col is None:
        print("  ⚠️ No company ID column found - creating sample data")
        return create_sample_companies()
    
    # Rename to standard column name
    if company_id_col != 'company_id':
        df = df.rename(columns={company_id_col: 'company_id'})
    
    # Clean company names
    if 'company_name' in df.columns:
        df['company_name'] = df['company_name'].astype(str).str.strip()
    else:
        df['company_name'] = df['company_id']  # Use ID as name if missing
    
    # Convert numeric columns
    numeric_cols = ['face_value', 'book_value']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add sector mapping (simplified - you can expand this)
    sector_map = {
        'TCS': 'IT', 'INFY': 'IT', 'WIPRO': 'IT', 'HCLTECH': 'IT', 'TECHM': 'IT',
        'HDFCBANK': 'Banking', 'ICICIBANK': 'Banking', 'SBIN': 'Banking', 
        'KOTAKBANK': 'Banking', 'AXISBANK': 'Banking',
        'RELIANCE': 'Energy', 'ONGC': 'Energy',
        'TATAMOTORS': 'Auto', 'MARUTI': 'Auto', 'M&M': 'Auto',
        'BAJFINANCE': 'NBFC', 'BAJAJFINSV': 'NBFC',
        'SUNPHARMA': 'Pharma', 'DRREDDY': 'Pharma',
        'HINDUNILVR': 'FMCG', 'ITC': 'FMCG'
    }
    
    # Use the correct column name for mapping
    if 'company_id' in df.columns:
        df['sector'] = df['company_id'].map(sector_map)
    else:
        df['sector'] = 'Other'
    
    # Select and rename columns for output
    output_cols = ['company_id', 'company_name', 'sector', 'face_value', 'book_value']
    existing_cols = [col for col in output_cols if col in df.columns]
    df = df[existing_cols]
    
    # Save cleaned data
    output_file = CLEAN_DATA_DIR / 'companies_clean.csv'
    df.to_csv(output_file, index=False)
    print(f"  ✅ Saved {len(df)} cleaned companies to {output_file}")
    
    return df

def create_sample_companies():
    """Create sample companies for testing"""
    print("  📝 Creating sample companies...")
    
    sample_companies = pd.DataFrame([
        {'company_id': 'TCS', 'company_name': 'Tata Consultancy Services', 'sector': 'IT', 'face_value': 1, 'book_value': 250},
        {'company_id': 'INFY', 'company_name': 'Infosys Limited', 'sector': 'IT', 'face_value': 5, 'book_value': 180},
        {'company_id': 'WIPRO', 'company_name': 'Wipro Limited', 'sector': 'IT', 'face_value': 2, 'book_value': 120},
        {'company_id': 'HDFCBANK', 'company_name': 'HDFC Bank', 'sector': 'Banking', 'face_value': 1, 'book_value': 450},
        {'company_id': 'RELIANCE', 'company_name': 'Reliance Industries', 'sector': 'Energy', 'face_value': 10, 'book_value': 800},
        {'company_id': 'ICICIBANK', 'company_name': 'ICICI Bank', 'sector': 'Banking', 'face_value': 2, 'book_value': 300},
        {'company_id': 'SBIN', 'company_name': 'State Bank of India', 'sector': 'Banking', 'face_value': 1, 'book_value': 280},
        {'company_id': 'HCLTECH', 'company_name': 'HCL Technologies', 'sector': 'IT', 'face_value': 2, 'book_value': 150},
        {'company_id': 'TATAMOTORS', 'company_name': 'Tata Motors', 'sector': 'Auto', 'face_value': 2, 'book_value': 95},
        {'company_id': 'SUNPHARMA', 'company_name': 'Sun Pharma', 'sector': 'Pharma', 'face_value': 1, 'book_value': 110},
    ])
    
    output_file = CLEAN_DATA_DIR / 'companies_clean.csv'
    sample_companies.to_csv(output_file, index=False)
    print(f"  ✅ Created {len(sample_companies)} sample companies")
    
    return sample_companies

def create_sample_profit_loss():
    """Create sample profit & loss data for demonstration"""
    print("\n📈 Creating sample profit & loss data...")
    
    # Sample companies from our list
    companies = ['TCS', 'INFY', 'WIPRO', 'HCLTECH', 'RELIANCE', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'TATAMOTORS', 'SUNPHARMA']
    years = ['Mar 2024', 'Mar 2023', 'Mar 2022', 'Mar 2021']
    
    data = []
    for company in companies:
        for year in years:
            # Generate realistic-looking random data
            base_sales = {
                'TCS': 240000, 'INFY': 150000, 'WIPRO': 90000, 'HCLTECH': 120000,
                'RELIANCE': 800000, 'HDFCBANK': 180000, 'ICICIBANK': 150000,
                'SBIN': 400000, 'TATAMOTORS': 350000, 'SUNPHARMA': 45000
            }.get(company, 100000)
            
            growth = {'Mar 2024': 1.15, 'Mar 2023': 1.12, 'Mar 2022': 1.08, 'Mar 2021': 1.05}
            sales = base_sales * growth.get(year, 1.0)
            
            data.append({
                'company_id': company,
                'year': year,
                'sales': round(sales, 0),
                'net_profit': round(sales * np.random.uniform(0.15, 0.25), 0),
                'opm_pct': round(np.random.uniform(18, 32), 2),
                'eps': round(np.random.uniform(30, 120), 2)
            })
    
    df = pd.DataFrame(data)
    output_file = CLEAN_DATA_DIR / 'profitandloss_clean.csv'
    df.to_csv(output_file, index=False)
    print(f"  ✅ Created {len(df)} sample profit & loss records")
    
    return df

def create_sample_balance_sheet():
    """Create sample balance sheet data"""
    print("\n📊 Creating sample balance sheet data...")
    
    companies = ['TCS', 'INFY', 'WIPRO', 'HCLTECH', 'RELIANCE', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'TATAMOTORS', 'SUNPHARMA']
    years = ['Mar 2024', 'Mar 2023', 'Mar 2022', 'Mar 2021']
    
    data = []
    for company in companies:
        for year in years:
            base_assets = {
                'TCS': 800000, 'INFY': 500000, 'WIPRO': 300000, 'HCLTECH': 400000,
                'RELIANCE': 5000000, 'HDFCBANK': 2000000, 'ICICIBANK': 1800000,
                'SBIN': 6000000, 'TATAMOTORS': 3500000, 'SUNPHARMA': 200000
            }.get(company, 500000)
            
            data.append({
                'company_id': company,
                'year': year,
                'total_assets': round(base_assets * np.random.uniform(0.95, 1.1), 0),
                'borrowings': round(base_assets * np.random.uniform(0.1, 0.4), 0),
                'debt_to_equity': round(np.random.uniform(0.2, 1.8), 2)
            })
    
    df = pd.DataFrame(data)
    output_file = CLEAN_DATA_DIR / 'balancesheet_clean.csv'
    df.to_csv(output_file, index=False)
    print(f"  ✅ Created {len(df)} sample balance sheet records")
    
    return df

def main():
    print("\n" + "="*60)
    print("🧹 CLEANING AND TRANSFORMATION")
    print("="*60)
    
    # Clean data (will create samples if raw data missing)
    clean_companies()
    create_sample_profit_loss()
    create_sample_balance_sheet()
    
    print(f"\n✅ Clean data saved to: {CLEAN_DATA_DIR}")
    print("\n📋 Files created:")
    for file in CLEAN_DATA_DIR.glob('*.csv'):
        size = file.stat().st_size
        print(f"   - {file.name} ({size:,} bytes)")

if __name__ == "__main__":
    main()