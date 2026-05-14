from django.db import models

class DimCompany(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    company_name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True, null=True)
    face_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    book_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'nifty_api_dimcompany'
    
    def __str__(self):
        return f"{self.symbol} - {self.company_name}"

class DimYear(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_label = models.CharField(max_length=20, unique=True)
    
    class Meta:
        managed = False
        db_table = 'nifty_api_dimyear'
    
    def __str__(self):
        return self.year_label

class FactProfitLoss(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(DimCompany, on_delete=models.DO_NOTHING, db_column='symbol')
    year = models.ForeignKey(DimYear, on_delete=models.DO_NOTHING, db_column='year_id')
    sales = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    net_profit = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    opm_pct = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'nifty_api_factprofitloss'
    
    def __str__(self):
        return f"{self.symbol.symbol} - {self.year.year_label}"
