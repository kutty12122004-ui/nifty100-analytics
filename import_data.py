import pandas as pd
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
django.setup()

from nifty_api.models import DimCompany, DimYear, FactProfitLoss

def clear_existing_data():
    """Clear existing P&L data to avoid duplicates"""
    print("🗑️ Clearing existing P&L data...")
    count = FactProfitLoss.objects.count()
    FactProfitLoss.objects.all().delete()
    print(f"   Deleted {count} existing records")

def populate_years():
    """Populate DimYear table with all years from 2000 to 2025"""
    print("📅 Populating DimYear table...")
    
    # Clear existing DimYear data first
    DimYear.objects.all().delete()
    
    years_created = 0
    for year in range(2000, 2026):
        year_label = str(year)
        DimYear.objects.create(year_label=year_label)
        years_created += 1
    
    print(f"✅ DimYear populated with {DimYear.objects.count()} years (2000-2025)")

def import_profit_loss():
    print("\n📊 Importing Profit & Loss data...")
    
    # Read the Excel file with headers
    df = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss')
    
    # Skip the first row (title row) and use the next row as headers
    # The headers are at row 1 (index 1)
    df = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=1)
    
    print(f"Found {len(df)} rows in Excel")
    print(f"Columns: {list(df.columns)}")
    
    # Get all companies as dict for quick lookup
    companies = {c.symbol: c for c in DimCompany.objects.all()}
    print(f"Found {len(companies)} companies in database")
    
    # Get all years as dict
    years = {int(y.year_label): y for y in DimYear.objects.all()}
    print(f"Found {len(years)} years in database")
    
    success = 0
    skipped = 0
    company_not_found = set()
    year_not_found = set()
    
    for index, row in df.iterrows():
        try:
            # Get company symbol
            symbol = str(row['company_id']).strip()
            
            # Skip if company doesn't exist
            if symbol not in companies:
                company_not_found.add(symbol)
                skipped += 1
                continue
            
            # Parse year
            year_str = str(row['year'])
            if 'TTM' in year_str or 'ttm' in year_str.lower():
                skipped += 1
                continue
            
            # Extract year number
            year_match = re.search(r'\d{4}', year_str)
            if not year_match:
                skipped += 1
                continue
            
            year_num = int(year_match.group())
            
            # Check if year exists
            if year_num not in years:
                year_not_found.add(year_num)
                skipped += 1
                continue
            
            # Get financial values (handle NaN values)
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
            
            # Calculate net profit margin
            net_profit_margin = (net_profit / sales * 100) if sales > 0 else 0
            
            # Get the objects
            company_obj = companies[symbol]
            year_obj = years[year_num]
            
            # Update or create record
            obj, created = FactProfitLoss.objects.update_or_create(
                symbol=company_obj,
                year=year_obj,
                defaults={
                    'sales': sales,
                    'net_profit': net_profit,
                    'opm_pct': opm_pct,
                    'eps': eps,
                    'net_profit_margin_pct': net_profit_margin,
                }
            )
            success += 1
            
            if success % 100 == 0:
                print(f"  Processed {success} records...")
                
        except Exception as e:
            print(f"  ❌ Error at row {index}: {e}")
            continue
    
    print(f"\n✅ P&L Import complete:")
    print(f"   Success: {success} records added")
    print(f"   Skipped: {skipped} records")
    if company_not_found:
        print(f"   Companies not found: {list(company_not_found)[:10]}...")
    if year_not_found:
        print(f"   Years not found: {list(year_not_found)}")

def verify_import():
    print("\n📊 Verifying imported data...")
    
    total_pl = FactProfitLoss.objects.count()
    print(f"Total P&L Records: {total_pl}")
    
    if total_pl > 0:
        from django.db.models import Sum, Avg
        
        # Show sample records
        sample_records = FactProfitLoss.objects.select_related('symbol', 'year').values(
            'symbol__symbol', 'year__year_label', 'sales', 'net_profit', 'opm_pct'
        )[:10]
        print("\nSample records:")
        for record in sample_records:
            print(f"  {record['symbol__symbol']} - {record['year__year_label']}: "
                  f"Sales={record['sales']:,.0f}, Profit={record['net_profit']:,.0f}, OPM={record['opm_pct']:.1f}%")
        
        # Calculate totals for latest year (2024)
        year_2024 = DimYear.objects.filter(year_label='2024').first()
        if year_2024:
            latest_data = FactProfitLoss.objects.filter(year=year_2024)
            if latest_data.exists():
                total_revenue = latest_data.aggregate(Sum('sales'))['sales__sum'] or 0
                total_profit = latest_data.aggregate(Sum('net_profit'))['net_profit__sum'] or 0
                avg_opm = latest_data.aggregate(Avg('opm_pct'))['opm_pct__avg'] or 0
                
                print(f"\n📈 Dashboard Statistics (2024):")
                print(f"   Total Revenue: ₹{total_revenue:,.0f} Cr")
                print(f"   Total Profit: ₹{total_profit:,.0f} Cr")
                print(f"   Average OPM: {avg_opm:.1f}%")
    else:
        print("❌ No records were imported!")

if __name__ == '__main__':
    print("="*50)
    print("NIFTY 100 FINANCIAL DATA IMPORT")
    print("="*50)
    
    if not os.path.exists('profitandloss.xlsx'):
        print("❌ profitandloss.xlsx not found!")
        exit(1)
    
    # Step 1: Clear existing data
    clear_existing_data()
    
    # Step 2: Populate DimYear table
    populate_years()
    
    # Step 3: Import P&L data
    import_profit_loss()
    
    # Step 4: Verify
    verify_import()
    
    print("\n" + "="*50)
    print("IMPORT COMPLETE")
    print("="*50)