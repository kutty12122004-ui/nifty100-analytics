import pandas as pd
import re
from django.core.management.base import BaseCommand
from django.db.models import Sum
from nifty_api.models import DimCompany, DimYear, FactProfitLoss, FactBalanceSheet

class Command(BaseCommand):
    help = 'Import all data from Excel files'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("📊 IMPORTING NIFTY 100 COMPLETE DATA")
        self.stdout.write("=" * 60)

        # ========== 1. IMPORT COMPANIES ==========
        self.stdout.write("\n🏢 1. Importing Companies...")
        
        try:
            df_companies = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)
            self.stdout.write(f"   Found {len(df_companies)} companies")
            
            companies_created = 0
            for _, row in df_companies.iterrows():
                symbol = str(row.get('id', '')).strip()
                if not symbol or symbol == 'nan':
                    continue
                    
                company, created = DimCompany.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        'company_name': str(row.get('company_name', ''))[:200],
                        'sector': 'Other',
                        'sub_sector': None,
                        'website': str(row.get('website', '')) if pd.notna(row.get('website')) else None,
                        'nse_url': str(row.get('nse_profile', '')) if pd.notna(row.get('nse_profile')) else None,
                        'bse_url': str(row.get('bse_profile', '')) if pd.notna(row.get('bse_profile')) else None,
                        'face_value': float(row.get('face_value', 0)) if pd.notna(row.get('face_value')) else None,
                        'book_value': float(row.get('book_value', 0)) if pd.notna(row.get('book_value')) else None,
                    }
                )
                companies_created += 1
                
            self.stdout.write(self.style.SUCCESS(f"   ✅ Imported {companies_created} companies"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Error: {e}"))

        # ========== 2. IMPORT YEARS ==========
        self.stdout.write("\n📅 2. Importing Years...")
        
        DimYear.objects.all().delete()
        years_created = 0
        for year in range(2000, 2026):
            DimYear.objects.create(year_label=str(year))
            years_created += 1
        self.stdout.write(self.style.SUCCESS(f"   ✅ Created {years_created} years (2000-2025)"))

        # ========== 3. IMPORT PROFIT & LOSS ==========
        self.stdout.write("\n📈 3. Importing Profit & Loss Data...")
        
        try:
            df_pl = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=1)
            self.stdout.write(f"   Found {len(df_pl)} records")
            
            companies = {c.symbol: c for c in DimCompany.objects.all()}
            years = {int(y.year_label): y for y in DimYear.objects.all()}
            
            pl_created = 0
            pl_skipped = 0
            
            for _, row in df_pl.iterrows():
                symbol = str(row.get('company_id', '')).strip()
                if symbol not in companies:
                    pl_skipped += 1
                    continue
                
                year_str = str(row.get('year', ''))
                year_match = re.search(r'\d{4}', year_str)
                if not year_match:
                    pl_skipped += 1
                    continue
                
                year_num = int(year_match.group())
                if year_num not in years:
                    pl_skipped += 1
                    continue
                
                def safe_float(val):
                    return float(val) if pd.notna(val) else None
                
                FactProfitLoss.objects.update_or_create(
                    symbol=companies[symbol],
                    year=years[year_num],
                    defaults={
                        'sales': safe_float(row.get('sales', 0)),
                        'net_profit': safe_float(row.get('net_profit', 0)),
                        'opm_pct': safe_float(row.get('opm_percentage', 0)),
                        'eps': safe_float(row.get('eps', 0)),
                        'net_profit_margin_pct': safe_float(row.get('net_profit_margin', 0)) or None,
                    }
                )
                pl_created += 1
                
                if pl_created % 100 == 0:
                    self.stdout.write(f"      Imported {pl_created} records...")
            
            self.stdout.write(self.style.SUCCESS(f"   ✅ Imported {pl_created} P&L records (skipped {pl_skipped})"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Error: {e}"))

        # ========== 4. IMPORT BALANCE SHEET ==========
        self.stdout.write("\n📊 4. Importing Balance Sheet Data...")
        
        try:
            df_bs = pd.read_excel('balancesheet.xlsx', sheet_name='Balance Sheet', header=1)
            self.stdout.write(f"   Found {len(df_bs)} records")
            
            companies = {c.symbol: c for c in DimCompany.objects.all()}
            years = {int(y.year_label): y for y in DimYear.objects.all()}
            
            bs_created = 0
            bs_skipped = 0
            
            for _, row in df_bs.iterrows():
                symbol = str(row.get('company_id', '')).strip()
                if symbol not in companies:
                    bs_skipped += 1
                    continue
                
                year_str = str(row.get('year', ''))
                year_match = re.search(r'\d{4}', year_str)
                if not year_match:
                    bs_skipped += 1
                    continue
                
                year_num = int(year_match.group())
                if year_num not in years:
                    bs_skipped += 1
                    continue
                
                def safe_float(val):
                    return float(val) if pd.notna(val) else None
                
                FactBalanceSheet.objects.update_or_create(
                    symbol=companies[symbol],
                    year=years[year_num],
                    defaults={
                        'equity_capital': safe_float(row.get('equity_capital', 0)),
                        'reserves': safe_float(row.get('reserves', 0)),
                        'borrowings': safe_float(row.get('borrowings', 0)),
                        'total_liabilities': safe_float(row.get('total_liabilities', 0)),
                        'fixed_assets': safe_float(row.get('fixed_assets', 0)),
                        'total_assets': safe_float(row.get('total_assets', 0)),
                    }
                )
                bs_created += 1
                
                if bs_created % 100 == 0:
                    self.stdout.write(f"      Imported {bs_created} records...")
            
            self.stdout.write(self.style.SUCCESS(f"   ✅ Imported {bs_created} Balance Sheet records (skipped {bs_skipped})"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Error: {e}"))

        # ========== 5. VERIFICATION ==========
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 VERIFICATION")
        self.stdout.write("=" * 60)
        self.stdout.write(f"   Companies: {DimCompany.objects.count()}")
        self.stdout.write(f"   Years: {DimYear.objects.count()}")
        self.stdout.write(f"   P&L Records: {FactProfitLoss.objects.count()}")
        self.stdout.write(f"   Balance Sheet Records: {FactBalanceSheet.objects.count()}")
        
        total_sales = FactProfitLoss.objects.aggregate(total=Sum('sales'))['total'] or 0
        self.stdout.write(f"\n💰 Total Revenue in Database: ₹{total_sales:,.0f} Cr")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("✅ IMPORT COMPLETE!")
        self.stdout.write("=" * 60)
