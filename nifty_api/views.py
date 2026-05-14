from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from .models import DimCompany, DimYear, FactProfitLoss

def health_check(request):
    return JsonResponse({"status": "ok", "companies": DimCompany.objects.count()})

def api_root(request):
    return JsonResponse({"message": "Nifty 100 API", "total_companies": DimCompany.objects.count()})

def company_list(request):
    companies = DimCompany.objects.all().values("symbol", "company_name", "sector")
    return JsonResponse(list(companies), safe=False)

def company_detail(request, symbol):
    try:
        company = DimCompany.objects.get(symbol=symbol.upper())
        return JsonResponse({"symbol": company.symbol, "company_name": company.company_name, "sector": company.sector})
    except DimCompany.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

def top_performers(request):
    companies = FactProfitLoss.objects.values("symbol__symbol", "symbol__company_name").annotate(
        profit=Sum("net_profit")
    ).order_by("-profit")[:15]
    return JsonResponse({"top_performers": list(companies)})

def dashboard(request):
    context = {
        "total_companies": DimCompany.objects.count(),
        "total_sectors": DimCompany.objects.exclude(sector="").values("sector").distinct().count(),
        "pl_count": FactProfitLoss.objects.count(),
        "years_count": DimYear.objects.count(),
        "total_revenue": "0",
        "avg_opm": "0%",
    }
    return render(request, "dashboard.html", context)

def companies_list_page(request):
    return render(request, "companies.html", {"companies": DimCompany.objects.all()})

def company_detail_page(request, symbol):
    return render(request, "company_detail.html", {"symbol": symbol})

def top_performers_page(request):
    return render(request, "top_performers.html")

def sector_analysis_page(request):
    return render(request, "sector_analysis.html")
