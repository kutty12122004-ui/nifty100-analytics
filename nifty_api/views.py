from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Count, F, Value, FloatField, Q
from django.db.models.functions import Coalesce
from .models import DimCompany, DimYear, FactProfitLoss, FactBalanceSheet

def dashboard(request):
    """Dashboard view with real financial data"""
    companies = DimCompany.objects.all()
    total_companies = companies.count()
    
    # Count sectors (exclude empty/null sectors)
    sectors_count = companies.exclude(sector='').exclude(sector__isnull=True).values('sector').distinct().count()
    
    # Get the latest year (2024)
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        # Get financial data for 2024
        yearly_data = FactProfitLoss.objects.filter(year=latest_year)
        
        total_revenue = yearly_data.aggregate(total=Coalesce(Sum('sales'), Value(0)))['total'] or 0
        total_profit = yearly_data.aggregate(total=Coalesce(Sum('net_profit'), Value(0)))['total'] or 0
        avg_opm = yearly_data.aggregate(avg=Coalesce(Avg('opm_pct'), Value(0)))['avg'] or 0
        
        # Get top 10 companies by net profit for 2024
        top_companies = yearly_data.select_related('symbol').order_by('-net_profit')[:10]
        top_companies_list = []
        for item in top_companies:
            top_companies_list.append({
                'name': item.symbol.company_name,
                'symbol': item.symbol.symbol,
                'sector': item.symbol.sector or 'N/A',
                'net_profit': item.net_profit,
                'sales': item.sales,
                'opm': item.opm_pct,
            })
    else:
        total_revenue = 0
        total_profit = 0
        avg_opm = 0
        top_companies_list = []
    
    # Format revenue for display
    if total_revenue >= 1000:
        formatted_revenue = f"{total_revenue/1000:.1f}L Cr"
    else:
        formatted_revenue = f"{total_revenue:.0f} Cr"
    
    context = {
        'total_companies': total_companies,
        'total_sectors': sectors_count if sectors_count > 0 else 12,
        'total_revenue': formatted_revenue,
        'avg_opm': round(avg_opm, 1),
        'top_companies': top_companies_list,
    }
    return render(request, 'dashboard.html', context)

def companies_list_page(request):
    """Companies list page with financial summaries for latest year"""
    companies = DimCompany.objects.all()
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    companies_with_finance = []
    for company in companies:
        if latest_year:
            financial = FactProfitLoss.objects.filter(symbol=company, year=latest_year).first()
            companies_with_finance.append({
                'company': company,
                'sales': financial.sales if financial else 0,
                'net_profit': financial.net_profit if financial else 0,
                'opm_pct': financial.opm_pct if financial else 0,
            })
        else:
            companies_with_finance.append({
                'company': company,
                'sales': 0,
                'net_profit': 0,
                'opm_pct': 0,
            })
    
    context = {'companies_with_finance': companies_with_finance}
    return render(request, 'companies.html', context)

def company_detail_page(request, symbol):
    """Company detail page with complete financials"""
    company = get_object_or_404(DimCompany, symbol=symbol)
    
    # Get all profit loss statements for this company, ordered by year
    profit_loss = FactProfitLoss.objects.filter(symbol=company).select_related('year').order_by('-year__year_label')
    
    # Calculate key metrics
    latest_pl = profit_loss.first()
    
    # Get all available years for chart
    years_data = []
    sales_data = []
    profit_data = []
    opm_data = []
    
    for pl in profit_loss:
        years_data.append(pl.year.year_label)
        sales_data.append(float(pl.sales))
        profit_data.append(float(pl.net_profit))
        opm_data.append(float(pl.opm_pct))
    
    context = {
        'company': company,
        'profit_loss': profit_loss,
        'latest_pl': latest_pl,
        'years_data': years_data,
        'sales_data': sales_data,
        'profit_data': profit_data,
        'opm_data': opm_data,
    }
    return render(request, 'company_detail.html', context)

def top_performers_page(request):
    """Top performers page based on net profit for latest year"""
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        # Get top 15 companies by net profit
        top_companies_data = FactProfitLoss.objects.filter(year=latest_year).select_related('symbol').order_by('-net_profit')[:15]
        
        top_companies = []
        for item in top_companies_data:
            top_companies.append({
                'company': item.symbol,
                'sales': item.sales,
                'net_profit': item.net_profit,
                'opm_pct': item.opm_pct,
                'eps': item.eps,
            })
    else:
        top_companies = []
    
    context = {'companies': top_companies}
    return render(request, 'top_performers.html', context)

def sector_analysis_page(request):
    """Sector analysis page with aggregated financials for latest year"""
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        # Aggregate by sector
        sectors_data = FactProfitLoss.objects.filter(year=latest_year).select_related('symbol').values(
            'symbol__sector'
        ).annotate(
            companies=Count('symbol', distinct=True),
            total_sales=Coalesce(Sum('sales'), Value(0)),
            total_profit=Coalesce(Sum('net_profit'), Value(0)),
            avg_opm=Coalesce(Avg('opm_pct'), Value(0)),
        ).exclude(symbol__sector='').exclude(symbol__sector__isnull=True).order_by('-total_sales')
        
        sectors = []
        for sector in sectors_data:
            sectors.append({
                'sector': sector['symbol__sector'],
                'companies': sector['companies'],
                'total_sales': sector['total_sales'],
                'total_profit': sector['total_profit'],
                'avg_opm': round(sector['avg_opm'], 1),
            })
        
        # Calculate totals
        total_companies = sum(s['companies'] for s in sectors)
        total_revenue = sum(s['total_sales'] for s in sectors)
        total_profit = sum(s['total_profit'] for s in sectors)
        
        # Find best performing sector
        best_sector = max(sectors, key=lambda x: x['avg_opm']) if sectors else None
        
        context = {
            'sectors': sectors,
            'total_sectors': len(sectors),
            'total_companies': total_companies,
            'total_revenue': total_revenue,
            'total_profit': total_profit,
            'best_sector': best_sector,
        }
    else:
        context = {
            'sectors': [],
            'total_sectors': 0,
            'total_companies': 0,
            'total_revenue': 0,
            'total_profit': 0,
            'best_sector': None,
        }
    
    return render(request, 'sector_analysis.html', context)

# API Endpoints

def api_root(request):
    """API root"""
    return JsonResponse({
        'message': 'Nifty 100 Analytics API',
        'endpoints': {
            'companies': '/api/companies/',
            'companies_full': '/api/companies/all/',
            'sector_analysis': '/api/sector-analysis/',
            'dashboard_stats': '/api/dashboard-stats/',
            'company_detail': '/api/company/<symbol>/',
            'health': '/api/health/',
        }
    })

def api_company_list(request):
    """API: List all companies with basic info"""
    companies = DimCompany.objects.all().values(
        'symbol', 'company_name', 'sector', 'sub_sector', 
        'website', 'face_value', 'book_value'
    )
    return JsonResponse(list(companies), safe=False)

def api_companies_full(request):
    """API: List all companies with latest financial data"""
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        companies = []
        for company in DimCompany.objects.all():
            financial = FactProfitLoss.objects.filter(symbol=company, year=latest_year).first()
            companies.append({
                'symbol': company.symbol,
                'company_name': company.company_name,
                'sector': company.sector,
                'sales': float(financial.sales) if financial else 0,
                'net_profit': float(financial.net_profit) if financial else 0,
                'opm_pct': float(financial.opm_pct) if financial else 0,
                'eps': float(financial.eps) if financial else 0,
            })
    else:
        companies = []
    
    return JsonResponse(companies, safe=False)

def api_sector_analysis(request):
    """API: Sector analysis with financial aggregates for latest year"""
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

def api_dashboard_stats(request):
    """API: Dashboard statistics for latest year"""
    latest_year = DimYear.objects.filter(year_label='2024').first()
    
    if latest_year:
        yearly_data = FactProfitLoss.objects.filter(year=latest_year)
        
        total_revenue = yearly_data.aggregate(total=Coalesce(Sum('sales'), Value(0)))['total']
        total_profit = yearly_data.aggregate(total=Coalesce(Sum('net_profit'), Value(0)))['total']
        avg_opm = yearly_data.aggregate(avg=Coalesce(Avg('opm_pct'), Value(0)))['avg']
        
        # Get top sector
        top_sector_data = yearly_data.select_related('symbol').values('symbol__sector').annotate(
            total_rev=Coalesce(Sum('sales'), Value(0))
        ).exclude(symbol__sector='').exclude(symbol__sector__isnull=True).order_by('-total_rev').first()
        
        # Format revenue
        if total_revenue >= 1000:
            formatted_revenue = f"{total_revenue/1000:.1f}L Cr"
        else:
            formatted_revenue = f"{total_revenue:.0f} Cr"
        
        return JsonResponse({
            'total_companies': DimCompany.objects.count(),
            'total_sectors': DimCompany.objects.exclude(sector='').exclude(sector__isnull=True).values('sector').distinct().count(),
            'total_revenue': formatted_revenue,
            'avg_opm': round(float(avg_opm), 1),
            'top_sector': top_sector_data['symbol__sector'] if top_sector_data else 'N/A',
        })
    else:
        return JsonResponse({
            'total_companies': DimCompany.objects.count(),
            'total_sectors': 0,
            'total_revenue': '0 Cr',
            'avg_opm': 0,
            'top_sector': 'N/A',
        })

def api_company_detail(request, symbol):
    """API: Company detail with historical financials"""
    company = get_object_or_404(DimCompany, symbol=symbol)
    
    profit_loss = FactProfitLoss.objects.filter(symbol=company).select_related('year').order_by('year__year_label')
    
    historical_data = []
    for pl in profit_loss:
        historical_data.append({
            'year': pl.year.year_label,
            'sales': float(pl.sales),
            'net_profit': float(pl.net_profit),
            'opm_pct': float(pl.opm_pct),
            'eps': float(pl.eps),
        })
    
    return JsonResponse({
        'symbol': company.symbol,
        'company_name': company.company_name,
        'sector': company.sector,
        'website': company.website,
        'historical_data': historical_data,
    })

def api_health(request):
    """API: Health check"""
    return JsonResponse({
        'status': 'ok',
        'companies_count': DimCompany.objects.count(),
        'profit_loss_records': FactProfitLoss.objects.count(),
        'latest_year': DimYear.objects.order_by('-year_label').first().year_label if DimYear.objects.exists() else None,
    })