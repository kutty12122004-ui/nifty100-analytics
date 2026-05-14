import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from .models import DimCompany, DimYear, FactProfitLoss, FactBalanceSheet

# ========== HELPER FUNCTIONS ==========

def load_all_companies():
    """Load all companies from database"""
    return DimCompany.objects.all()

def get_financial_summary():
    """Get aggregated financial data from database"""
    pl_data = FactProfitLoss.objects.aggregate(
        total_revenue=Sum('sales'),
        total_profit=Sum('net_profit'),
        avg_opm=Avg('opm_pct')
    )
    return {
        'total_revenue': pl_data.get('total_revenue') or 0,
        'total_profit': pl_data.get('total_profit') or 0,
        'avg_opm': pl_data.get('avg_opm') or 0
    }

# ========== API VIEWS ==========

def health_check(request):
    """API health check endpoint"""
    return JsonResponse({
        "status": "ok",
        "message": "Nifty 100 API is running",
        "companies": DimCompany.objects.count(),
        "pl_records": FactProfitLoss.objects.count(),
        "bs_records": FactBalanceSheet.objects.count()
    })

def api_root(request):
    """API root endpoint with all endpoints"""
    return JsonResponse({
        "message": "Nifty 100 Financial Intelligence API",
        "version": "2.0",
        "endpoints": {
            "health": "/api/health/",
            "companies": "/api/companies/",
            "company_detail": "/api/companies/{symbol}/",
            "top_performers": "/api/top-performers/",
            "sector_analysis": "/api/sector-analysis/",
        }
    })

def company_list(request):
    """Get all companies"""
    companies = DimCompany.objects.all().values(
        'symbol', 'company_name', 'sector', 'face_value', 'book_value'
    )
    return JsonResponse({
        "success": True,
        "total": len(companies),
        "companies": list(companies)
    })

def company_detail(request, symbol):
    """Get detailed information for a specific company"""
    try:
        company = DimCompany.objects.get(symbol=symbol.upper())
        
        # Get latest financial data
        latest_pl = FactProfitLoss.objects.filter(
            symbol=company
        ).order_by('-year__year_label').first()
        
        latest_bs = FactBalanceSheet.objects.filter(
            symbol=company
        ).order_by('-year__year_label').first()
        
        result = {
            "symbol": company.symbol,
            "company_name": company.company_name,
            "sector": company.sector,
            "face_value": float(company.face_value) if company.face_value else None,
            "book_value": float(company.book_value) if company.book_value else None,
        }
        
        if latest_pl:
            result["latest_financials"] = {
                "year": latest_pl.year.year_label,
                "sales": float(latest_pl.sales) if latest_pl.sales else 0,
                "net_profit": float(latest_pl.net_profit) if latest_pl.net_profit else 0,
                "opm_pct": float(latest_pl.opm_pct) if latest_pl.opm_pct else 0
            }
        
        if latest_bs:
            result["balance_sheet"] = {
                "total_assets": float(latest_bs.total_assets) if latest_bs.total_assets else 0,
                "total_liabilities": float(latest_bs.total_liabilities) if latest_bs.total_liabilities else 0
            }
        
        return JsonResponse(result)
    except DimCompany.DoesNotExist:
        return JsonResponse({"error": f"Company {symbol} not found"}, status=404)

def top_performers(request):
    """Get top 20 companies by net profit"""
    top_companies = FactProfitLoss.objects.values(
        'symbol__symbol', 'symbol__company_name', 'symbol__sector'
    ).annotate(
        net_profit=Sum('net_profit')
    ).order_by('-net_profit')[:20]
    
    result = []
    for idx, company in enumerate(top_companies, 1):
        result.append({
            "rank": idx,
            "symbol": company['symbol__symbol'],
            "company_name": company['symbol__company_name'],
            "sector": company['symbol__sector'],
            "net_profit_cr": float(company['net_profit']) if company['net_profit'] else 0
        })
    
    return JsonResponse({"top_performers": result})

def sector_analysis(request):
    """Get sector-wise analysis"""
    sector_data = FactProfitLoss.objects.values(
        'symbol__sector'
    ).annotate(
        total_revenue=Sum('sales'),
        total_profit=Sum('net_profit'),
        avg_opm=Avg('opm_pct'),
        companies=Count('symbol', distinct=True)
    ).order_by('-total_profit')
    
    result = []
    for sector in sector_data:
        if sector['symbol__sector']:
            result.append({
                "sector": sector['symbol__sector'],
                "total_revenue_cr": float(sector['total_revenue']) if sector['total_revenue'] else 0,
                "total_profit_cr": float(sector['total_profit']) if sector['total_profit'] else 0,
                "avg_opm_pct": float(sector['avg_opm']) if sector['avg_opm'] else 0,
                "companies": sector['companies']
            })
    
    return JsonResponse({"sectors": result})

# ========== PAGE VIEWS ==========

def dashboard(request):
    """Main dashboard page"""
    financial = get_financial_summary()
    
    context = {
        "total_companies": DimCompany.objects.count(),
        "total_sectors": DimCompany.objects.exclude(sector='').values('sector').distinct().count(),
        "total_revenue": f"{financial['total_revenue'] / 100000:.1f}L Cr" if financial['total_revenue'] > 0 else "0",
        "avg_opm": f"{financial['avg_opm']:.1f}%" if financial['avg_opm'] > 0 else "0%",
        "pl_count": FactProfitLoss.objects.count(),
        "bs_count": FactBalanceSheet.objects.count(),
        "years_count": DimYear.objects.count(),
    }
    return render(request, "dashboard.html", context)

def companies_list_page(request):
    """Companies list page"""
    companies = DimCompany.objects.all().order_by('company_name')
    return render(request, "companies.html", {"companies": companies})

def company_detail_page(request, symbol):
    """Company detail page"""
    company = DimCompany.objects.filter(symbol=symbol.upper()).first()
    return render(request, "company_detail.html", {"company": company, "symbol": symbol.upper()})

def top_performers_page(request):
    """Top performers page"""
    return render(request, "top_performers.html")

def sector_analysis_page(request):
    """Sector analysis page"""
    return render(request, "sector_analysis.html")
