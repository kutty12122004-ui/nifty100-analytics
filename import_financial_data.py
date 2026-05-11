import pandas as pd
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
django.setup()

from nifty_api.models import DimCompany, FactProfitLoss

def import_profit_loss():
    print("📊 Importing Profit & Loss data...")
    
    # Read the Excel file - skip first 3 rows (title and headers)
    df = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=None, skiprows=3)
    
    # Define column indices based on your data
    # 0: id, 1: company_id, 2: year, 3: sales, 4: expenses, 5: operating_profit, 
    # 6: opm_percentage, 7: other_income, 8: interest, 9: depreciation, 
    # 10: profit_before_tax, 11: tax_percentage, 12: net_profit, 13: eps, 14: dividend_payout
    
    success = 0
    skipped = 0
    not_found = 0
    
    # Create a cache of company objects to avoid repeated DB queries
    company_cache = {}
    
    for index in range(len(df)):
        row = df.iloc[index]
        
        # Skip empty rows
        if pd.isna(row[1]):
            skipped += 1
            continue
            
        try:
            # Get company symbol
            symbol = str(row[1]).strip()
            
            # Skip TTM entries
            year_val = row[2]
            if pd.isna(year_val):
                skipped += 1
                continue
            
            year_str = str(year_val)
            if 'TTM' in year_str or 'ttm' in year_str.lower():
                skipped += 1
                continue
            
            # Parse year
            try:
                if 'Dec' in year_str:
                    year = int(year_str.split()[1])
                elif 'Mar' in year_str:
                    year = int(year_str.split()[1])
                elif 'Sep' in year_str:
                    year = int(year_str.split()[1])
                else:
                    year_match = re.search(r'\d{4}', year_str)
                    if year_match:
                        year = int(year_match.group())
                    else:
                        year = int(float(year_str))
            except:
                skipped += 1
                continue
            
            # Get financial values
            def safe_float(val):
                if pd.isna(val):
                    return 0.0
                try:
                    return float(val)
                except:
                    return 0.0
            
            sales = safe_float(row[3])
            net_profit = safe_float(row[12]) if len(row) > 12 else 0
            opm_pct = safe_float(row[6])
            eps = safe_float(row[13]) if len(row) > 13 else 0
            
            # Calculate net profit margin
            net_profit_margin = (net_profit / sales * 100) if sales > 0 else 0
            
            # Get the DimCompany object (cache it for performance)
            if symbol not in company_cache:
                try:
                    company_cache[symbol] = DimCompany.objects.get(symbol=symbol)
                except DimCompany.DoesNotExist:
                    print(f"  ⚠️ Company {symbol} not found in DimCompany, skipping...")
                    not_found += 1
                    continue
            
            company = company_cache[symbol]
            
            # Update or create record - NOTE: 'symbol' here is the ForeignKey field name
            obj, created = FactProfitLoss.objects.update_or_create(
                symbol=company,  # Pass the DimCompany object, not the string
                year=year,
                defaults={
                    'sales': sales,
                    'net_profit': net_profit,
                    'opm_pct': opm_pct,
                    'eps': eps,
                    'net_profit_margin_pct': net_profit_margin,
                }
            )
            success += 1
            
            if success % 50 == 0:
                print(f"  Processed {success} records... (Current: {symbol} {year})")
                
        except Exception as e:
            print(f"  ❌ Error at row {index}: {e}")
            continue
    
    print(f"\n✅ P&L Import complete: {success} added, {skipped} skipped, {not_found} companies not found")
    
    # Clear the cache
    company_cache.clear()

def update_dashboard_stats():
    print("\n📊 Checking imported data...")
    
    total_pl = FactProfitLoss.objects.count()
    print(f"Total P&L Records: {total_pl}")
    
    if total_pl > 0:
        from django.db.models import Sum, Avg
        
        # Get latest year
        latest_year_data = FactProfitLoss.objects.order_by('-year').values('year').first()
        if latest_year_data:
            latest_year = latest_year_data['year']
            print(f"\nLatest year with data: {latest_year}")
            
            latest_data = FactProfitLoss.objects.filter(year=latest_year)
            total_revenue = latest_data.aggregate(Sum('sales'))['sales__sum'] or 0
            total_profit = latest_data.aggregate(Sum('net_profit'))['net_profit__sum'] or 0
            avg_opm = latest_data.aggregate(Avg('opm_pct'))['opm_pct__avg'] or 0
            
            print(f"Total Revenue (latest year): ₹{total_revenue:,.0f} Cr")
            print(f"Total Profit (latest year): ₹{total_profit:,.0f} Cr")
            print(f"Average OPM: {avg_opm:.1f}%")
        
        # Show sample records
        sample_records = FactProfitLoss.objects.select_related('symbol').values('symbol__symbol', 'year', 'sales', 'net_profit')[:10]
        print("\nSample records:")
        for record in sample_records:
            print(f"  {record['symbol__symbol']} - {record['year']}: Sales={record['sales']:,.0f}, Profit={record['net_profit']:,.0f}")
    else:
        print("❌ No records were imported!")

if __name__ == '__main__':
    print("="*50)
    print("NIFTY 100 FINANCIAL DATA IMPORT")
    print("="*50)
    
    if not os.path.exists('profitandloss.xlsx'):
        print("❌ profitandloss.xlsx not found!")
        exit(1)
    
    import_profit_loss()
    update_dashboard_stats()
    
    print("\n" + "="*50)
    print("IMPORT COMPLETE")
    print("="*50)