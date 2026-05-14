from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from .models import DimCompany, DimYear, FactProfitLoss

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "companies": DimCompany.objects.count(),
        "pl_records": FactProfitLoss.objects.count()
    })

def api_root(request):
    return JsonResponse({
        "message": "Nifty 100 Financial Intelligence API",
        "total_companies": DimCompany.objects.count()
    })

def company_list(request):
    companies = DimCompany.objects.all().values("symbol", "company_name", "sector", "face_value", "book_value")
    return JsonResponse({"success": True, "total": len(companies), "companies": list(companies)})

def company_detail(request, symbol):
    try:
        company = DimCompany.objects.get(symbol=symbol.upper())
        return JsonResponse({
            "symbol": company.symbol,
            "company_name": company.company_name,
            "sector": company.sector,
            "face_value": float(company.face_value) if company.face_value else None,
            "book_value": float(company.book_value) if company.book_value else None,
        })
    except DimCompany.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

def top_performers(request):
    # Get latest year
    latest_year = DimYear.objects.order_by('-year_label').first()
    if latest_year:
        top = FactProfitLoss.objects.filter(year=latest_year).values(
            "symbol__symbol", "symbol__company_name", "symbol__sector"
        ).annotate(
            profit=Sum("net_profit"),
            opm=Avg("opm_pct")
        ).order_by("-profit")[:15]
    else:
        top = FactProfitLoss.objects.values(
            "symbol__symbol", "symbol__company_name", "symbol__sector"
        ).annotate(
            profit=Sum("net_profit"),
            opm=Avg("opm_pct")
        ).order_by("-profit")[:15]
    
    result = []
    for idx, t in enumerate(top, 1):
        result.append({
            "rank": idx,
            "symbol": t["symbol__symbol"],
            "company_name": t["symbol__company_name"],
            "sector": t["symbol__sector"],
            "profit_cr": float(t["profit"]) if t["profit"] else 0,
            "opm_pct": float(t["opm"]) if t["opm"] else 0
        })
    return JsonResponse({"top_performers": result})

def sector_analysis(request):
    sectors = FactProfitLoss.objects.values("symbol__sector").annotate(
        total_revenue=Sum("sales"),
        total_profit=Sum("net_profit"),
        avg_opm=Avg("opm_pct"),
        companies_count=Count("symbol", distinct=True)
    ).order_by("-total_profit")
    
    result = []
    for s in sectors:
        if s["symbol__sector"]:
            result.append({
                "sector": s["symbol__sector"],
                "total_revenue_cr": float(s["total_revenue"]) if s["total_revenue"] else 0,
                "total_profit_cr": float(s["total_profit"]) if s["total_profit"] else 0,
                "avg_opm": float(s["avg_opm"]) if s["avg_opm"] else 0,
                "companies": s["companies_count"]
            })
    return JsonResponse({"sectors": result})

def dashboard(request):
    companies = DimCompany.objects.all()
    total_companies = companies.count()
    sectors_count = companies.exclude(sector="").values("sector").distinct().count()
    pl_count = FactProfitLoss.objects.count()
    years_count = DimYear.objects.count()
    
    financial = FactProfitLoss.objects.aggregate(
        total_sales=Sum("sales"),
        avg_opm=Avg("opm_pct")
    )
    
    total_sales = financial.get("total_sales") or 0
    avg_opm = financial.get("avg_opm") or 0
    
    context = {
        "total_companies": total_companies,
        "total_sectors": sectors_count,
        "total_revenue": f"{total_sales / 100000:.1f}L Cr" if total_sales > 0 else "0",
        "avg_opm": f"{avg_opm:.1f}%",
        "pl_count": pl_count,
        "bs_count": 0,
        "years_count": years_count,
    }
    return render(request, "dashboard.html", context)

def companies_list_page(request):
    companies = DimCompany.objects.all().order_by("company_name")
    return render(request, "companies.html", {"companies": companies})

def company_detail_page(request, symbol):
    company = DimCompany.objects.filter(symbol=symbol.upper()).first()
    return render(request, "company_detail.html", {"company": company, "symbol": symbol.upper()})

def top_performers_page(request):
    return render(request, "top_performers.html")

def sector_analysis_page(request):
    return render(request, "sector_analysis.html")
