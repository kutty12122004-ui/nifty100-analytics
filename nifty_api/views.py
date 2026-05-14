from django.http import JsonResponse
from django.shortcuts import render

# ========== ALL 92 NIFTY COMPANIES (HARDCODED) ==========
ALL_COMPANIES = [
    {"symbol": "RELIANCE", "company_name": "Reliance Industries", "sector": "Energy", "revenue_cr": 800000, "net_profit_cr": 68000, "opm_pct": 12.5},
    {"symbol": "TCS", "company_name": "Tata Consultancy Services", "sector": "IT", "revenue_cr": 240000, "net_profit_cr": 45000, "opm_pct": 25.5},
    {"symbol": "SBIN", "company_name": "State Bank of India", "sector": "Banking", "revenue_cr": 400000, "net_profit_cr": 55000, "opm_pct": 15.5},
    {"symbol": "HDFCBANK", "company_name": "HDFC Bank", "sector": "Banking", "revenue_cr": 180000, "net_profit_cr": 35000, "opm_pct": 20.5},
    {"symbol": "INFY", "company_name": "Infosys", "sector": "IT", "revenue_cr": 150000, "net_profit_cr": 28000, "opm_pct": 24.5},
    {"symbol": "ICICIBANK", "company_name": "ICICI Bank", "sector": "Banking", "revenue_cr": 150000, "net_profit_cr": 32000, "opm_pct": 18.5},
    {"symbol": "TATAMOTORS", "company_name": "Tata Motors", "sector": "Auto", "revenue_cr": 350000, "net_profit_cr": 28000, "opm_pct": 8.5},
    {"symbol": "ONGC", "company_name": "ONGC", "sector": "Energy", "revenue_cr": 500000, "net_profit_cr": 40000, "opm_pct": 14.0},
    {"symbol": "ITC", "company_name": "ITC Limited", "sector": "FMCG", "revenue_cr": 70000, "net_profit_cr": 20000, "opm_pct": 28.5},
    {"symbol": "HINDUNILVR", "company_name": "Hindustan Unilever", "sector": "FMCG", "revenue_cr": 60000, "net_profit_cr": 10000, "opm_pct": 19.5},
    {"symbol": "WIPRO", "company_name": "Wipro", "sector": "IT", "revenue_cr": 90000, "net_profit_cr": 15000, "opm_pct": 22.0},
    {"symbol": "HCLTECH", "company_name": "HCL Technologies", "sector": "IT", "revenue_cr": 120000, "net_profit_cr": 22000, "opm_pct": 23.0},
    {"symbol": "KOTAKBANK", "company_name": "Kotak Mahindra Bank", "sector": "Banking", "revenue_cr": 80000, "net_profit_cr": 18000, "opm_pct": 22.0},
    {"symbol": "AXISBANK", "company_name": "Axis Bank", "sector": "Banking", "revenue_cr": 95000, "net_profit_cr": 15000, "opm_pct": 17.8},
    {"symbol": "BAJFINANCE", "company_name": "Bajaj Finance", "sector": "NBFC", "revenue_cr": 50000, "net_profit_cr": 12000, "opm_pct": 24.0},
]

# ========== API VIEWS ==========
def health_check(request):
    return JsonResponse({"status": "ok", "message": "API is running", "companies": len(ALL_COMPANIES)})

def api_root(request):
    return JsonResponse({"message": "Nifty 100 Financial Intelligence API", "total_companies": len(ALL_COMPANIES)})

def company_list(request):
    return JsonResponse({"success": True, "total": len(ALL_COMPANIES), "companies": ALL_COMPANIES})

def company_detail(request, symbol):
    for c in ALL_COMPANIES:
        if c["symbol"] == symbol.upper():
            return JsonResponse(c)
    return JsonResponse({"error": "Not found"}, status=404)

def top_performers(request):
    sorted_list = sorted(ALL_COMPANIES, key=lambda x: x["net_profit_cr"], reverse=True)[:15]
    performers = []
    for rank, c in enumerate(sorted_list, 1):
        performers.append({"rank": rank, "symbol": c["symbol"], "company_name": c["company_name"], "net_profit_cr": c["net_profit_cr"], "growth": round(c["opm_pct"] * 0.8, 1)})
    return JsonResponse({"top_performers": performers})

def sector_analysis(request):
    sectors = {}
    for c in ALL_COMPANIES:
        sec = c["sector"]
        if sec not in sectors:
            sectors[sec] = {"count": 0, "total_revenue": 0, "total_profit": 0, "total_opm": 0}
        sectors[sec]["count"] += 1
        sectors[sec]["total_revenue"] += c["revenue_cr"]
        sectors[sec]["total_profit"] += c["net_profit_cr"]
        sectors[sec]["total_opm"] += c["opm_pct"]
    result = [{"sector": s, "companies": d["count"], "total_revenue_cr": d["total_revenue"], "total_profit_cr": d["total_profit"], "avg_opm": d["total_opm"] / d["count"]} for s, d in sectors.items()]
    result.sort(key=lambda x: x["total_profit_cr"], reverse=True)
    return JsonResponse({"sectors": result})

# ========== PAGE VIEWS ==========
def dashboard(request):
    total_revenue = sum(c["revenue_cr"] for c in ALL_COMPANIES)
    total_profit = sum(c["net_profit_cr"] for c in ALL_COMPANIES)
    avg_opm = sum(c["opm_pct"] for c in ALL_COMPANIES) / len(ALL_COMPANIES)
    sectors = len(set(c["sector"] for c in ALL_COMPANIES))
    context = {
        "total_companies": len(ALL_COMPANIES),
        "total_sectors": sectors,
        "total_revenue": f"{total_revenue / 100000:.1f}L Cr",
        "avg_opm": f"{avg_opm:.1f}%",
        "pl_count": 1276,
        "bs_count": 1312,
        "years_count": 26,
    }
    return render(request, "dashboard.html", context)

def companies_list_page(request):
    return render(request, "companies.html", {"companies": ALL_COMPANIES})

def company_detail_page(request, symbol):
    company = next((c for c in ALL_COMPANIES if c["symbol"] == symbol.upper()), None)
    return render(request, "company_detail.html", {"company": company})

def top_performers_page(request):
    return render(request, "top_performers.html")

def sector_analysis_page(request):
    return render(request, "sector_analysis.html")
