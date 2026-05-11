import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Check if we're on Render
ON_RENDER = os.environ.get('RENDER', False)

try:
    django.setup()
except Exception as e:
    print(f"Django setup error: {e}")
    sys.exit(1)

from nifty_api.models import DimCompany, DimYear, FactProfitLoss
import pandas as pd
import re

def import_profit_loss():
    """Import P&L data from Excel file"""
    
    # Check if data already exists
    if FactProfitLoss.objects.count() > 0:
        print(f"✅ Data already loaded: {FactProfitLoss.objects.count()} records")
        return
    
    excel_path = 'profitandloss.xlsx'
    if not os.path.exists(excel_path):
        print(f"❌ Excel file not found: {excel_path}")
        return
    
    print("📊 Importing Profit & Loss data...")
    
    try:
        df = pd.read_excel(excel_path, header=1)
        print(f"Found {len(df)} rows in Excel")
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return
    
    # Get companies and years
    companies = {c.symbol: c for c in DimCompany.objects.all()}
    
    # Ensure years exist
    years_dict = {}
    for year in range(2000, 2026):
        year_obj, created = DimYear.objects.get_or_create(year_label=str(year))
        years_dict[year] = year_obj
    
    success = 0
    
    for index, row in df.iterrows():
        try:
            symbol = str(row['company_id']).strip()
            
            if symbol not in companies:
                continue
            
            # Parse year
            year_str = str(row['year'])
            if 'TTM' in year_str:
                continue
            
            year_match = re.search(r'\d{4}', year_str)
            if not year_match:
                continue
            
            year_num = int(year_match.group())
            
            if year_num not in years_dict:
                continue
            
            # Get values
            def safe_float(val):
                if pd.isna(val):
                    return 0.0
                try:
                    return float(val)
                except:
                    return 0.0
            
            sales = safe_float(row.get('sales', 0))
            net_profit = safe_float(row.get('net_profit', 0))
            opm_pct = safe_float(row.get('opm_percentage', 0))
            eps = safe_float(row.get('eps', 0))
            
            # Calculate OPM if needed
            if sales > 0 and opm_pct == 0:
                opm_pct = (net_profit / sales) * 100
            
            FactProfitLoss.objects.update_or_create(
                symbol=companies[symbol],
                year=years_dict[year_num],
                defaults={
                    'sales': sales,
                    'net_profit': net_profit,
                    'opm_pct': opm_pct,
                    'eps': eps,
                }
            )
            success += 1
            
            if success % 200 == 0:
                print(f"  Processed {success} records...")
                
        except Exception as e:
            continue
    
    print(f"✅ Imported {success} P&L records")

def update_company_sectors():
    """Update company sectors based on names"""
    industries = {
        'BANK': 'Banking',
        'FINANCE': 'Financial Services',
        'INSURANCE': 'Insurance',
        'TECH': 'Technology',
        'INFO': 'Technology',
        'PHARMA': 'Pharmaceuticals',
        'LAB': 'Pharmaceuticals',
        'AUTO': 'Automobile',
        'MOTOR': 'Automobile',
        'ENERGY': 'Energy',
        'POWER': 'Power',
        'GAS': 'Oil & Gas',
        'OIL': 'Oil & Gas',
        'STEEL': 'Metals & Mining',
        'ALCO': 'Metals & Mining',
        'CEMENT': 'Cement',
        'CONSUMER': 'FMCG',
        'PAINT': 'Chemicals',
    }
    
    updated = 0
    for company in DimCompany.objects.all():
        if company.sector:
            continue
        
        for keyword, sector in industries.items():
            if keyword in company.company_name.upper():
                company.sector = sector
                company.save()
                updated += 1
                break
        
        if not company.sector:
            company.sector = 'Others'
            company.save()
            updated += 1
    
    print(f"✅ Updated {updated} companies with sector info")

if __name__ == '__main__':
    print("=" * 50)
    print("LOADING INITIAL DATA")
    print("=" * 50)
    
    import_profit_loss()
    update_company_sectors()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Companies: {DimCompany.objects.count()}")
    print(f"P&L Records: {FactProfitLoss.objects.count()}")
    print(f"Years: {DimYear.objects.count()}")
    print("\n✅ Data loading complete!")