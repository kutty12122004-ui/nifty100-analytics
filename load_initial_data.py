import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
django.setup()

from nifty_api.models import DimCompany, FactProfitLoss
from django.core import management

print(f"Current state:")
print(f"  Companies: {DimCompany.objects.count()}")
print(f"  P&L Records: {FactProfitLoss.objects.count()}")

# Load data if database is mostly empty
if DimCompany.objects.count() < 50:
    print("\nLoading complete dataset from JSON...")
    try:
        management.call_command('loaddata', 'nifty100_complete_data.json')
        print(f"✅ Data loaded successfully!")
        print(f"  Companies: {DimCompany.objects.count()}")
        print(f"  P&L Records: {FactProfitLoss.objects.count()}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
else:
    print("✅ Database already populated")
    print(f"  Companies: {DimCompany.objects.count()}")
    print(f"  P&L Records: {FactProfitLoss.objects.count()}")