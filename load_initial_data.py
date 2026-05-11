import os
import sys
import django

# Setup Django environment
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

    # --- 1. Load DimYear if it's empty ---
    if DimYear.objects.count() == 0:
        print("📅 Populating DimYear table...")
        for year in range(2000, 2026):
            DimYear.objects.get_or_create(year_label=str(year))
        print(f"✅ DimYear populated with {DimYear.objects.count()} years")
    else:
        print(f"✅ DimYear already has {DimYear.objects.count()} years")

    # --- 2. Load DimCompany if it's empty ---
    if DimCompany.objects.count() == 0:
        print("📊 Loading companies from companies.xlsx...")
        try:
            df_companies = pd.read_excel('companies.xlsx', skiprows=2)
            companies_loaded = 0
            for _, row in df_companies.iterrows():
                symbol = row['id']
                company_name = str(row['company_name']).split('<')[0].strip()
                DimCompany.objects.get_or_create(
                    symbol=symbol,
                    defaults={'company_name': company_name, 'sector': 'Other'}
                )
                companies_loaded += 1
            print(f"✅ Loaded {companies_loaded} companies")
        except FileNotFoundError:
            print("⚠️ companies.xlsx not found, skipping company import.")
        except Exception as e:
            print(f"Error loading companies: {e}")
    else:
        print(f"✅ DimCompany already has {DimCompany.objects.count()} companies")

    # --- 3. Load FactProfitLoss if it's empty ---
    if FactProfitLoss.objects.count() == 0:
        print("📊 Importing Profit & Loss data...")
        companies = {c.symbol: c for c in DimCompany.objects.all()}
        years = {y.year_label: y for y in DimYear.objects.all()}
        success = 0

        try:
            df_pl = pd.read_excel('profitandloss.xlsx', header=1)
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

                # Safely get values
                def safe_float(val):
                    return float(val) if pd.notna(val) else 0.0

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
                except Exception:
                    continue
            print(f"✅ Imported {success} P&L records")
        except Exception as e:
            print(f"Error importing P&L data: {e}")
    else:
        print(f"✅ FactProfitLoss already has {FactProfitLoss.objects.count()} records")

    # --- 4. Update sector for a few companies for a better initial dashboard ---
    print("🏭 Updating sector information for a few companies...")
    sector_updates = {
        'RELIANCE': 'Energy & Telecom',
        'TCS': 'Information Technology',
        'HDFCBANK': 'Banking',
        'INFY': 'Information Technology',
        'ICICIBANK': 'Banking',
        'ITC': 'FMCG',
        'SBIN': 'Banking',
    }
    updated = 0
    for symbol, sector in sector_updates.items():
        try:
            company = DimCompany.objects.get(symbol=symbol)
            if not company.sector or company.sector == 'Other':
                company.sector = sector
                company.save()
                updated += 1
        except DimCompany.DoesNotExist:
            continue
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