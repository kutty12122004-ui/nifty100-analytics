from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from .models import DimCompany, DimYear, FactProfitLoss, FactBalanceSheet

def health_check(request):
    return JsonResponse({"status": "ok", "message": "API is running", "companies": DimCompany.objects.count()})

def api_root(request):
    return JsonResponse({
        "message": "Nifty 100 Financial Intelligence API",
        "endpoints": {
            "health": "/api/health/",
            "companies": "/api/companies/",
        }
    })

def company_list(request):
    companies = DimCompany.objects.all().values("symbol", "company_name", "sector", "face_value", "book_value")
    return JsonResponse(list(companies), safe=False)

def dashboard(request):
    total_companies = DimCompany.objects.count()
    sectors_count = DimCompany.objects.exclude(sector="").values("sector").distinct().count()
    
    # REAL COUNTS FROM DATABASE
    pl_count = FactProfitLoss.objects.count()
    bs_count = FactBalanceSheet.objects.count()
    years_count = DimYear.objects.count()
    
    financial_data = FactProfitLoss.objects.aggregate(
        total_sales=Sum("sales"),
        total_profit=Sum("net_profit"),
        avg_opm=Avg("opm_pct")
    )
    
    total_sales = financial_data.get("total_sales") or 0
    avg_opm = financial_data.get("avg_opm") or 0
    
    if total_sales > 0:
        formatted_revenue = f"{total_sales / 100000:.1f}L Cr"
    else:
        formatted_revenue = "0"
    
    context = {
        "total_companies": total_companies,
        "total_sectors": sectors_count if sectors_count > 0 else 1,
        "total_revenue": formatted_revenue,
        "avg_opm": f"{avg_opm:.1f}%",
        "pl_count": pl_count,
        "bs_count": bs_count,
        "years_count": years_count,
    }
    return render(request, "dashboard.html", context)

def companies_list_page(request):
    return render(request, "companies.html")

def company_detail_page(request, symbol):
    return render(request, "company_detail.html", {"symbol": symbol})

def top_performers_page(request):
    return render(request, "top_performers.html")

def sector_analysis_page(request):
    return render(request, "sector_analysis.html")
