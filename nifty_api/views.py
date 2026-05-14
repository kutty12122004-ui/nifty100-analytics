from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Count, Q
from django.views.decorators.csrf import csrf_exempt
from .models import DimCompany, DimYear, FactProfitLoss, FactBalanceSheet

# ===================== API VIEWS =====================

def api_root(request):
    return JsonResponse({
        'message': 'Nifty 100 Financial Intelligence API',
        'endpoints': {
            'companies': '/api/companies/',
            'health': '/api/health/',
            'top_performers': '/api/top-performers/',
            'sector_analysis': '/api/sector-analysis/',
        }
    })

def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'API is running',
        'companies': DimCompany.objects.count()
    })

def company_list(request):
    companies = DimCompany.objects.values(
        'symbol', 'company_name', 'sector', 'sub_sector',
        'website', 'face_value', 'book_value'
    )
    return JsonResponse(list(companies), safe=False)

def company_detail(request, symbol):
    company = get_object_or_404(DimCompany, symbol=symbol.upper())
    return JsonResponse({
        'symbol': company.symbol,
        'company_name': company.company_name,
        'sector': company.sector,
    })

def top_performers(request):
    companies = DimCompany.objects.order_by('-book_value')[:20]
    data = [{'symbol': c.symbol, 'company_name': c.company_name, 'book_value': float(c.book_value or 0)} for c in companies]
    return JsonResponse({'top_performers': data})

def sector_analysis(request):
    sectors = DimCompany.objects.values('sector').annotate(
        count=Count('symbol')
    ).order_by('-count')
    return JsonResponse(list(sectors), safe=False)

# ===================== PAGE VIEWS =====================

def dashboard(request):
    companies = DimCompany.objects.all()
    total_companies = companies.count()
    sectors_count = companies.exclude(sector='').values('sector').distinct().count()
    if sectors_count == 0:
        sectors_count = 1

    latest_year = DimYear.objects.order_by('-sort_order').first()

    if latest_year:
        financial = FactProfitLoss.objects.filter(year=latest_year).aggregate(
            total_sales=Sum('sales'), total_profit=Sum('net_profit'), avg_opm=Avg('opm_pct')
        )
    else:
        financial = FactProfitLoss.objects.aggregate(
            total_sales=Sum('sales'), total_profit=Sum('net_profit'), avg_opm=Avg('opm_pct')
        )

    total_sales = financial.get('total_sales') or 0
    total_profit = financial.get('total_profit') or 0
    avg_opm = financial.get('avg_opm') or 0

    if avg_opm > 100 or avg_opm < 0:
        if total_sales > 0:
            avg_opm = (total_profit / total_sales) * 100

    formatted_revenue = f"{total_sales / 100000:.1f}L Cr" if total_sales > 0 else "0"

    context = {
        'total_companies': total_companies,
        'total_sectors': sectors_count,
        'total_revenue': formatted_revenue,
        'avg_opm': f"{avg_opm:.1f}%",
    }
    return render(request, 'dashboard.html', context)

def companies_list_page(request):
    return render(request, 'companies.html')

def company_detail_page(request, symbol):
    return render(request, 'company_detail.html', {'symbol': symbol})

def top_performers_page(request):
    return render(request, 'top_performers.html')

def sector_analysis_page(request):
    return render(request, 'sector_analysis.html')

# Force update - 05/13/2026 10:29:18
# Force update - 05/13/2026 11:07:27