import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
django.setup()

from nifty_api.models import DimCompany
import openpyxl

# Only load if database is empty
if DimCompany.objects.count() == 0:
    print("Loading companies from Excel...")
    wb = openpyxl.load_workbook('companies.xlsx')
    sheet = wb.active
    
    count = 0
    for i, row in enumerate(sheet.iter_rows(values_only=True), 1):
        if i <= 2:
            continue
        
        symbol = row[0]
        company_name = row[2]
        website = row[5] if row[5] else ''
        face_value = row[8] if row[8] else 0
        book_value = row[9] if row[9] else 0
        
        if symbol and company_name:
            DimCompany.objects.get_or_create(
                symbol=symbol,
                defaults={
                    'company_name': company_name,
                    'website': website,
                    'face_value': face_value,
                    'book_value': book_value,
                }
            )
            count += 1
    
    print(f"✅ Loaded {count} companies!")
else:
    print(f"✅ Database has {DimCompany.objects.count()} companies")