import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from nifty_api.models import DimCompany, DimYear, FactProfitLoss
import pandas as pd
import re

def load_initial_data():
    print("=" * 50)
    print("LOADING INITIAL DATA")
    print("=" * 50)

    # --- 1. Load DimYear ---
    if DimYear.objects.count() == 0:
        print("📅 Populating DimYear table...")
        for year in range(2000, 2026):
            DimYear.objects.get_or_create(year_label=str(year))
        print(f"✅ DimYear populated with {DimYear.objects.count()} years")
    else:
        print(f"✅ DimYear already has {DimYear.objects.count()} years")

    # --- 2. Load DimCompany from companies.xlsx ---
    if DimCompany.objects.count() == 0:
        print("📊 Loading companies from companies.xlsx...")
        try:
            # Skip first 2 rows (title and headers)
            df = pd.read_excel('companies.xlsx', skiprows=2, header=None)
            
            print(f"Found {len(df)} rows in companies file")
            
            companies_loaded = 0
            for _, row in df.iterrows():
                # Column 0: symbol, Column 2: company_name
                symbol = str(row[0]).strip()
                company_name = str(row[2]).split('<')[0].strip()
                
                if symbol and symbol != 'nan' and company_name != 'nan':
                    DimCompany.objects.get_or_create(
                        symbol=symbol,
                        defaults={
                            'company_name': company_name,
                            'sector': 'Other',
                            'face_value': float(row[8]) if pd.notna(row[8]) else None,
                            'book_value': float(row[9]) if pd.notna(row[9]) else None,
                        }
                    )
                    companies_loaded += 1
                    
            print(f"✅ Loaded {companies_loaded} companies")
        except Exception as e:
            print(f"Error loading companies: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"✅ DimCompany already has {DimCompany.objects.count()} companies")

    # --- 3. Load FactProfitLoss from profitandloss.xlsx ---
    if FactProfitLoss.objects.count() == 0:
        print("📊 Importing Profit & Loss data...")
        
        companies = {c.symbol: c for c in DimCompany.objects.all()}
        years = {y.year_label: y for y in DimYear.objects.all()}
        
        if len(companies) == 0:
            print("⚠️ No companies found, skipping P&L import")
        else:
            try:
                # Read P&L file with headers at row 1
                df_pl = pd.read_excel('profitandloss.xlsx', header=1)
                print(f"Found {len(df_pl)} rows in P&L file")
                
                success = 0
                for _, row in df_pl.iterrows():
                    symbol = str(row['company_id']).strip()
                    if symbol not in companies:
                        continue
                    
                    year_str = str(row['year'])
                    if 'TTM' in year_str:
                        continue
                    
                    year_match = re.search(r'\d{4}', year_str)
                    if not year_match:
                        continue
                    
                    year_num = year_match.group()
                    if year_num not in years:
                        continue
                    
                    def safe_float(val):
                        if pd.isna(val):
                            return 0.0
                        try:
                            return float(val)
                        except:
                            return 0.0
                    
                    try:
                        FactProfitLoss.objects.update_or_create(
                            symbol=companies[symbol],
                            year=years[year_num],
                            defaults={
                                'sales': safe_float(row.get('sales')),
                                'net_profit': safe_float(row.get('net_profit')),
                                'opm_pct': safe_float(row.get('opm_percentage')),
                                'eps': safe_float(row.get('eps')),
                            }
                        )
                        success += 1
                    except Exception as e:
                        continue
                
                print(f"✅ Imported {success} P&L records")
            except Exception as e:
                print(f"Error importing P&L data: {e}")
                import traceback
                traceback.print_exc()
    else:
        print(f"✅ FactProfitLoss already has {FactProfitLoss.objects.count()} records")

    # --- 4. Update sector information based on company names ---
    print("🏭 Updating sector information...")
    
    # Sector mapping based on keywords in company names
    sector_keywords = {
        'Banking': ['BANK', 'HDFC', 'ICICI', 'SBI', 'AXIS', 'KOTAK', 'PNB', 'INDUSIND', 'CANBK', 'BARODA'],
        'Information Technology': ['TECH', 'INFY', 'TCS', 'HCL', 'WIPRO', 'LTIM', 'MINDTREE', 'INFOEDGE'],
        'Pharmaceuticals': ['PHARMA', 'SUN', 'CIPLA', 'DRREDDY', 'DIVIS', 'TORRENT', 'ZYDUS', 'ABBOTT', 'APOLLO'],
        'Automobile': ['MOTOR', 'AUTO', 'MARUTI', 'TATAMOTORS', 'EICHER', 'HERO', 'BAJAJ AUTO', 'TVS', 'BOSCH', 'M&M'],
        'Energy & Power': ['ENERGY', 'POWER', 'ADANI GREEN', 'NTPC', 'POWERGRID', 'TATAPOWER', 'JSW ENERGY', 'NHPC'],
        'Oil & Gas': ['OIL', 'GAS', 'ONGC', 'BPCL', 'IOC', 'GAIL', 'RELIANCE'],
        'Metals & Mining': ['STEEL', 'ALCO', 'HINDALCO', 'JSWSTEEL', 'TATASTEEL', 'COAL', 'JINDAL', 'VEDL'],
        'Cement & Construction': ['CEMENT', 'CONSTRUCTION', 'AMBUJA', 'ULTRACEMCO', 'SHREE CEMENT', 'GRASIM', 'L&T'],
        'FMCG': ['CONSUMER', 'DABUR', 'BRITANNIA', 'NESTLE', 'HINDUNILVR', 'ITC', 'GODREJ', 'TITAN', 'PIDILITE'],
        'Telecom': ['TELECOM', 'BHARTI', 'AIRTL'],
    }
    
    updated = 0
    for company in DimCompany.objects.all():
        if not company.sector or company.sector == 'Other':
            name_upper = company.company_name.upper()
            for sector, keywords in sector_keywords.items():
                for keyword in keywords:
                    if keyword.upper() in name_upper:
                        company.sector = sector
                        company.save()
                        updated += 1
                        break
                if company.sector and company.sector != 'Other':
                    break
    
    print(f"✅ Updated {updated} companies with sector info")

    print("\n" + "=" * 50)
    print("DATA LOADING COMPLETE")
    print(f"Companies: {DimCompany.objects.count()}")
    print(f"P&L Records: {FactProfitLoss.objects.count()}")
    print(f"Years: {DimYear.objects.count()}")
    print("=" * 50)
    print("Starting server...")

if __name__ == '__main__':
    load_initial_data()