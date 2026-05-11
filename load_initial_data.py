import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
django.setup()

from django.core import management

# Load data if database is empty
from nifty_api.models import DimCompany

if DimCompany.objects.count() == 0:
    print("Loading initial data...")
    management.call_command('loaddata', 'nifty100_data.json')
    print(f"Loaded {DimCompany.objects.count()} companies!")
else:
    print(f"Database already has {DimCompany.objects.count()} companies")