from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# 23 Companies Data
ALL_COMPANIES = [
    {"symbol": "RELIANCE", "company_name": "Reliance Industries", "sector": "Energy", "revenue_cr": 800000, "net_profit_cr": 68000, "opm_pct": 12.5},
    {"symbol": "TCS", "company_name": "Tata Consultancy Services", "sector": "IT", "revenue_cr": 240000, "net_profit_cr": 45000, "opm_pct": 25.5},
    {"symbol": "SBIN", "company_name": "State Bank of India", "sector": "Banking", "revenue_cr": 400000, "net_profit_cr": 55000, "opm_pct": 15.5},
    {"symbol": "HDFCBANK", "company_name": "HDFC Bank", "sector": "Banking", "revenue_cr": 180000, "net_profit_cr": 35000, "opm_pct": 20.5},
    {"symbol": "INFY", "company_name": "Infosys", "sector": "IT", "revenue_cr": 150000, "net_profit_cr": 28000, "opm_pct": 24.5},
    {"symbol": "TATAMOTORS", "company_name": "Tata Motors", "sector": "Auto", "revenue_cr": 350000, "net_profit_cr": 28000, "opm_pct": 8.5},
    {"symbol": "ONGC", "company_name": "ONGC", "sector": "Energy", "revenue_cr": 500000, "net_profit_cr": 40000, "opm_pct": 14.0},
    {"symbol": "ICICIBANK", "company_name": "ICICI Bank", "sector": "Banking", "revenue_cr": 150000, "net_profit_cr": 32000, "opm_pct": 18.5},
    {"symbol": "WIPRO", "company_name": "Wipro", "sector": "IT", "revenue_cr": 90000, "net_profit_cr": 15000, "opm_pct": 22.0},
    {"symbol": "HCLTECH", "company_name": "HCL Technologies", "sector": "IT", "revenue_cr": 120000, "net_profit_cr": 22000, "opm_pct": 23.0},
    {"symbol": "KOTAKBANK", "company_name": "Kotak Mahindra Bank", "sector": "Banking", "revenue_cr": 80000, "net_profit_cr": 18000, "opm_pct": 22.0},
    {"symbol": "AXISBANK", "company_name": "Axis Bank", "sector": "Banking", "revenue_cr": 95000, "net_profit_cr": 15000, "opm_pct": 17.8},
    {"symbol": "BAJFINANCE", "company_name": "Bajaj Finance", "sector": "NBFC", "revenue_cr": 50000, "net_profit_cr": 12000, "opm_pct": 24.0},
    {"symbol": "ITC", "company_name": "ITC Limited", "sector": "FMCG", "revenue_cr": 70000, "net_profit_cr": 20000, "opm_pct": 28.5},
    {"symbol": "HINDUNILVR", "company_name": "Hindustan Unilever", "sector": "FMCG", "revenue_cr": 60000, "net_profit_cr": 10000, "opm_pct": 19.5},
    {"symbol": "SUNPHARMA", "company_name": "Sun Pharma", "sector": "Pharma", "revenue_cr": 45000, "net_profit_cr": 9000, "opm_pct": 20.0},
    {"symbol": "MARUTI", "company_name": "Maruti Suzuki", "sector": "Auto", "revenue_cr": 120000, "net_profit_cr": 10000, "opm_pct": 10.5},
    {"symbol": "TATASTEEL", "company_name": "Tata Steel", "sector": "Metals", "revenue_cr": 230000, "net_profit_cr": 15000, "opm_pct": 10.5},
    {"symbol": "POWERGRID", "company_name": "Power Grid Corp", "sector": "Energy", "revenue_cr": 45000, "net_profit_cr": 15000, "opm_pct": 35.0},
    {"symbol": "BHARTIARTL", "company_name": "Bharti Airtel", "sector": "Telecom", "revenue_cr": 150000, "net_profit_cr": 12000, "opm_pct": 18.5},
    {"symbol": "ULTRACEMCO", "company_name": "UltraTech Cement", "sector": "Cement", "revenue_cr": 65000, "net_profit_cr": 8000, "opm_pct": 16.5},
    {"symbol": "NESTLEIND", "company_name": "Nestle India", "sector": "FMCG", "revenue_cr": 18000, "net_profit_cr": 2500, "opm_pct": 16.0},
    {"symbol": "JSWSTEEL", "company_name": "JSW Steel", "sector": "Metals", "revenue_cr": 150000, "net_profit_cr": 10000, "opm_pct": 11.0},
]

@csrf_exempt
def api_root(request):
    return JsonResponse({"message": "API Working", "total": len(ALL_COMPANIES)})

@csrf_exempt
def company_list(request):
    return JsonResponse({"success": True, "total": len(ALL_COMPANIES), "companies": ALL_COMPANIES})

@csrf_exempt
def health_check(request):
    return JsonResponse({"status": "healthy", "message": "API is running"})

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
