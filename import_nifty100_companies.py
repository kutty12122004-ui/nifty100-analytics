# import_nifty100_companies.py
"""
Import all Nifty 100 companies from Excel file
Place this file in your D:\nifty100-analytics folder
"""

import os
import sys
import django
import csv
import openpyxl
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nifty100_project.settings')
django.setup()

from nifty_api.models import DimCompany

def import_from_excel():
    """Import companies directly from Excel file"""
    
    # Path to your uploaded Excel file - UPDATE THIS PATH
    excel_file = 'companies.xlsx'  # Put the file in your project root
    
    if not os.path.exists(excel_file):
        print(f"❌ Error: {excel_file} not found!")
        print(f"   Please place companies.xlsx in: {os.getcwd()}")
        return
    
    print("=" * 60)
    print("📊 Importing Nifty 100 Companies from Excel")
    print("=" * 60)
    
    # Load workbook
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active
    
    companies_imported = 0
    companies_updated = 0
    
    for i, row in enumerate(sheet.iter_rows(values_only=True), 1):
        # Skip title row (row 1) and header row (row 2)
        if i <= 2:
            continue
        
        # Extract data from row
        symbol = row[0]
        company_name = row[2]
        website = row[5] if row[5] else ''
        face_value = row[8] if row[8] else 0
        book_value = row[9] if row[9] else 0
        
        if not symbol or not company_name:
            continue
        
        # Create or update company
        company, created = DimCompany.objects.update_or_create(
            symbol=symbol,
            defaults={
                'company_name': company_name,
                'website': website,
                'face_value': Decimal(str(face_value)) if face_value else None,
                'book_value': Decimal(str(book_value)) if book_value else None,
                'sector': '',  # Excel doesn't have this
                'sub_sector': '',  # Excel doesn't have this
            }
        )
        
        if created:
            companies_imported += 1
            print(f"   ✅ Added: {symbol} - {company_name}")
        else:
            companies_updated += 1
            print(f"   🔄 Updated: {symbol} - {company_name}")
    
    print("=" * 60)
    print("📊 Import Summary")
    print("=" * 60)
    print(f"✅ New companies imported: {companies_imported}")
    print(f"🔄 Companies updated: {companies_updated}")
    print(f"📊 Total companies in database: {DimCompany.objects.count()}")
    print("=" * 60)
    
    # Show sample
    print("\n📋 Sample companies in database:")
    for company in DimCompany.objects.all()[:10]:
        print(f"   • {company.symbol}: {company.company_name}")
    
    print("\n✅ Import complete!")

if __name__ == '__main__':
    import_from_excel()
