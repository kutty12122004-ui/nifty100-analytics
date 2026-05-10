from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# ------------------------------
# 23 Companies Data
# ------------------------------
ALL_COMPANIES = [
    {"symbol": "RELIANCE", "company_name": "Reliance Industries", "sector": "Energy", "revenue_cr": 800000, "net_profit_cr": 68000, "opm_pct": 12.5},
    {"symbol": "TCS", "company_name": "Tata Consultancy Services", "sector": "IT", "revenue_cr": 240000, "net_profit_cr": 45000, "opm_pct": 25.5},
    {"symbol": "SBIN", "company_name": "State Bank of India", "sector": "Banking", "revenue_cr": 400000, "net_profit_cr": 55000, "opm_pct": 15.5},
    {"symbol": "HDFCBANK", "company_name": "HDFC Bank", "sector": "Banking", "revenue_cr": 180000, "net_profit_cr": 35000, "opm_pct": 20.5},
    {"symbol": "INFY", "company_name": "Infosys", "sector": "IT", "revenue_cr": 150000, "net_profit_cr": 28000, "opm_pct": 24.5},
    {"symbol": "TATAMOTORS", "company_name": "Tata Motors", "sector": "Auto", "revenue_cr": 350000, "net_profit_cr": 28000, "opm_pct": 8.5},
    {"symbol": "ONGC", "company_name": "ONGC", "sector": "Energy", "revenue_cr": 500000, "net_profit_cr": 40000, "opm_pct": 14.0},
    {"symbol": "ICICIBANK", "company_name": "ICICI Bank", "sector": "Banking", "revenue_cr": 150000, "net_profit_cr": 32000, "opm_pct": 18.5},
]

# ------------------------------
# API Views
# ------------------------------
@csrf_exempt
def health_check(request):
    return JsonResponse({"status": "healthy", "message": "API is running", "companies": len(ALL_COMPANIES)})

@csrf_exempt
def api_root(request):
    return JsonResponse({"message": "Nifty 100 API", "total_companies": len(ALL_COMPANIES)})

@csrf_exempt
def company_list(request):
    return JsonResponse({"success": True, "total": len(ALL_COMPANIES), "companies": ALL_COMPANIES})

@csrf_exempt
def company_detail(request, symbol):
    for c in ALL_COMPANIES:
        if c["symbol"] == symbol.upper():
            return JsonResponse(c)
    return JsonResponse({"error": "Company not found"}, status=404)

@csrf_exempt
def top_performers(request):
    sorted_list = sorted(ALL_COMPANIES, key=lambda x: x["net_profit_cr"], reverse=True)[:10]
    return JsonResponse({"metric": "net_profit", "top_performers": sorted_list})

@csrf_exempt
def sector_analysis(request):
    sectors = {}
    for c in ALL_COMPANIES:
        sec = c["sector"]
        if sec not in sectors:
            sectors[sec] = {"total_revenue": 0, "total_profit": 0, "companies": 0}
        sectors[sec]["total_revenue"] += c["revenue_cr"]
        sectors[sec]["total_profit"] += c["net_profit_cr"]
        sectors[sec]["companies"] += 1
    return JsonResponse({"sectors": sectors})

# ------------------------------
# Page Views
# ------------------------------
def dashboard(request):
    return render(request, "dashboard.html")

def companies_list_page(request):
    return render(request, "companies.html")

def company_detail_page(request, symbol):
    return render(request, "company_detail.html", {"symbol": symbol})

def top_performers_page(request):
    return render(request, "top_performers.html")

def sector_analysis_page(request):
    return render(request, "sector_analysis.html")
