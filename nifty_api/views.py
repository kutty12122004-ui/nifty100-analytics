from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Count, F, Value, Q
from django.db.models.functions import Coalesce
from .models import DimCompany, DimYear, FactProfitLoss, FactBalanceSheet

# ==================== FRONTEND PAGE VIEWS ====================

def dashboard(request):
    """Dashboard view with real financial data"""
    companies = DimCompany.objects.all()
    total_companies = companies.count()
    
    # Count sectors
    sectors_count = companies.exclude(sector='').exclude(sector__isnull=True).values('sector').distinct().count()
    
    # Get latest year
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        yearly_data = FactProfitLoss.objects.filter(year=latest_year)
        total_revenue = yearly_data.aggregate(total=Coalesce(Sum('sales'), Value(0)))['total'] or 0
        avg_opm = yearly_data.aggregate(avg=Coalesce(Avg('opm_pct'), Value(0)))['avg'] or 0
        
        if total_revenue >= 1000:
            formatted_revenue = f"{total_revenue/1000:.1f}L Cr"
        else:
            formatted_revenue = f"{total_revenue:.0f} Cr"
    else:
        formatted_revenue = "0 Cr"
        avg_opm = 0
    
    context = {
        'total_companies': total_companies,
        'total_sectors': sectors_count if sectors_count > 0 else 12,
        'total_revenue': formatted_revenue,
        'avg_opm': round(avg_opm, 1),
    }
    return render(request, 'dashboard.html', context)

def companies_list_page(request):
    """Companies list page"""
    companies = DimCompany.objects.all()
    context = {'companies': companies}
    return render(request, 'companies.html', context)

def company_detail_page(request, symbol):
    """Company detail page"""
    company = get_object_or_404(DimCompany, symbol=symbol)
    context = {'company': company}
    return render(request, 'company_detail.html', context)

def top_performers_page(request):
    """Top performers page"""
    companies = DimCompany.objects.all()[:10]
    context = {'companies': companies}
    return render(request, 'top_performers.html', context)

def sector_analysis_page(request):
    """Sector analysis page"""
    sectors = DimCompany.objects.values('sector').annotate(
        count=Count('symbol')
    ).exclude(sector='').exclude(sector__isnull=True).order_by('-count')
    context = {'sectors': sectors}
    return render(request, 'sector_analysis.html', context)

# ==================== API ENDPOINTS ====================

def api_root(request):
    """API root"""
    return JsonResponse({
        'message': 'Nifty 100 Analytics API',
        'endpoints': {
            'companies': '/api/companies/',
            'dashboard_stats': '/api/dashboard-stats/',
            'sector_analysis': '/api/sector-analysis/',
            'health': '/api/health/',
        }
    })

def api_company_list(request):
    """API: List all companies"""
    companies = DimCompany.objects.all().values(
        'symbol', 'company_name', 'sector', 'sub_sector', 
        'website', 'face_value', 'book_value'
    )
    return JsonResponse(list(companies), safe=False)

def api_dashboard_stats(request):
    """API: Dashboard statistics"""
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        yearly_data = FactProfitLoss.objects.filter(year=latest_year)
        total_revenue = yearly_data.aggregate(total=Coalesce(Sum('sales'), Value(0)))['total'] or 0
        avg_opm = yearly_data.aggregate(avg=Coalesce(Avg('opm_pct'), Value(0)))['avg'] or 0
        
        if total_revenue >= 1000:
            formatted_revenue = f"{total_revenue/1000:.1f}L Cr"
        else:
            formatted_revenue = f"{total_revenue:.0f} Cr"
        
        return JsonResponse({
            'total_companies': DimCompany.objects.count(),
            'total_sectors': DimCompany.objects.exclude(sector='').exclude(sector__isnull=True).values('sector').distinct().count(),
            'total_revenue': formatted_revenue,
            'avg_opm': round(avg_opm, 1),
        })
    else:
        return JsonResponse({
            'total_companies': DimCompany.objects.count(),
            'total_sectors': 0,
            'total_revenue': '0 Cr',
            'avg_opm': 0,
        })

def api_sector_analysis(request):
    """API: Sector analysis"""
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        sectors = FactProfitLoss.objects.filter(year=latest_year).select_related('symbol').values(
            'symbol__sector'
        ).annotate(
            companies=Count('symbol', distinct=True),
            total_sales_cr=Coalesce(Sum('sales'), Value(0)),
            total_profit_cr=Coalesce(Sum('net_profit'), Value(0)),
            avg_opm_pct=Coalesce(Avg('opm_pct'), Value(0)),
        ).exclude(symbol__sector='').exclude(symbol__sector__isnull=True).order_by('-total_sales_cr')
        
        sectors_list = []
        for sector in sectors:
            sectors_list.append({
                'sector': sector['symbol__sector'],
                'companies': sector['companies'],
                'total_sales_cr': float(sector['total_sales_cr']),
                'total_profit_cr': float(sector['total_profit_cr']),
                'avg_opm_pct': round(float(sector['avg_opm_pct']), 1),
            })
    else:
        sectors_list = []
    
    return JsonResponse({'sectors': sectors_list}, safe=False)

def api_health(request):
    """API: Health check"""
    return JsonResponse({
        'status': 'ok',
        'companies_count': DimCompany.objects.count(),
        'profit_loss_records': FactProfitLoss.objects.count(),
        'balance_sheet_records': FactBalanceSheet.objects.count(),
    })