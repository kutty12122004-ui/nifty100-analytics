# nifty_api/models.py
from django.db import models

class DimCompany(models.Model):
    """Company dimension table from your data warehouse"""
    symbol = models.CharField(max_length=20, primary_key=True)
    company_name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, null=True, blank=True)
    sub_sector = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)
    face_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    book_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    class Meta:
        managed = False  # Important: Don't let Django modify the table
        db_table = 'dim_company'  # Exact table name in PostgreSQL
    
    def __str__(self):
        return f"{self.symbol} - {self.company_name}"

class DimYear(models.Model):
    """Year dimension table"""
    year_id = models.AutoField(primary_key=True)
    year_label = models.CharField(max_length=20, unique=True)
    fiscal_year = models.IntegerField(null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'dim_year'
    
    def __str__(self):
        return self.year_label

class FactProfitLoss(models.Model):
    """Profit & Loss fact table"""
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(DimCompany, on_delete=models.DO_NOTHING, db_column='symbol')
    year = models.ForeignKey(DimYear, on_delete=models.DO_NOTHING, db_column='year_id')
    sales = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    net_profit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    opm_pct = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eps = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_profit_margin_pct = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'fact_profit_loss'
    
    def __str__(self):
        return f"{self.symbol.symbol} - {self.year.year_label}"

class FactBalanceSheet(models.Model):
    """Balance Sheet fact table"""
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(DimCompany, on_delete=models.DO_NOTHING, db_column='symbol')
    year = models.ForeignKey(DimYear, on_delete=models.DO_NOTHING, db_column='year_id')
    total_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    borrowings = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    debt_to_equity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'fact_balance_sheet'

class FactCashFlow(models.Model):
    """Cash Flow fact table"""
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(DimCompany, on_delete=models.DO_NOTHING, db_column='symbol')
    year = models.ForeignKey(DimYear, on_delete=models.DO_NOTHING, db_column='year_id')
    operating_activity = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    free_cash_flow = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'fact_cash_flow'