from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Count
from .models import DimCompany, FactProfitLoss, FactBalanceSheet

def dashboard(request):
    """Dashboard view"""
    companies = DimCompany.objects.all()
    total_companies = companies.count()
    
    # Count non-empty sectors
    sectors_count = companies.exclude(sector='').values('sector').distinct().count()
    if sectors_count == 0:
        sectors_count = 1  # Show at least 1 if we have companies
    
    context = {
        'total_companies': total_companies,
        'total_sectors': sectors_count,
        'total_revenue': 0,
        'avg_opm': 0,
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
    ).order_by('-count')
    context = {'sectors': sectors}
    return render(request, 'sector_analysis.html', context)

def api_root(request):
    """API root"""
    return JsonResponse({
        'message': 'Nifty 100 Analytics API',
        'endpoints': {
            'companies': '/api/companies/',
            'health': '/api/health/',
        }
    })

def company_list(request):
    """API: List all companies"""
    companies = DimCompany.objects.all().values(
        'symbol', 'company_name', 'sector', 'sub_sector', 
        'website', 'face_value', 'book_value'
    )
    return JsonResponse(list(companies), safe=False)

def health_check(request):
    """API: Health check"""
    return JsonResponse({
        'status': 'ok',
        'companies_count': DimCompany.objects.count()
    })