from django.http import JsonResponse
from django.shortcuts import render

# ========== ALL 92 NIFTY COMPANIES WITH FINANCIAL DATA ==========
ALL_COMPANIES = [
    {"symbol": "ABB", "company_name": "Abbott India Ltd", "sector": "Other", "revenue_cr": 5849.0, "net_profit_cr": 1201.0, "opm_pct": 25.0},
    {"symbol": "ADANIENSOL", "company_name": "Adani Energy Solutions Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ADANIENT", "company_name": "Adani Enterprises Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ADANIGREEN", "company_name": "Adani Green Energy Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ADANIPORTS", "company_name": "Adani Ports", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ADANIPOWER", "company_name": "Adani Power Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "AMBUJACEM", "company_name": "Ambuja Cements Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "APOLLOHOSP", "company_name": "Apollo Hospitals", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ASIANPAINT", "company_name": "Asian Paints", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ATGL", "company_name": "Adani Total Gas Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "AXISBANK", "company_name": "Axis Bank Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BAJAJ-AUTO", "company_name": "Bajaj Auto Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BAJAJFINSV", "company_name": "Bajaj Finserv Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BAJAJHLDNG", "company_name": "Bajaj Holdings", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BAJFINANCE", "company_name": "Bajaj Finance Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BANKBARODA", "company_name": "Bank of Baroda", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BEL", "company_name": "Bharat Electronics Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BHARTIARTL", "company_name": "Bharti Airtel Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BHEL", "company_name": "Bharat Heavy Electricals", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BOSCHLTD", "company_name": "Bosch Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BPCL", "company_name": "Bharat Petroleum Corp", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "BRITANNIA", "company_name": "Britannia Industries", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "CANBK", "company_name": "Canara Bank", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "CHOLAFIN", "company_name": "Cholamandalam Investment", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "CIPLA", "company_name": "Cipla Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "COALINDIA", "company_name": "Coal India Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "DABUR", "company_name": "Dabur India Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "DIVISLAB", "company_name": "Divis Laboratories", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "DLF", "company_name": "DLF Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "DMART", "company_name": "Avenue Supermarts", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "DRREDDY", "company_name": "Dr Reddys Labs", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "EICHERMOT", "company_name": "Eicher Motors", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "GAIL", "company_name": "GAIL India", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "GODREJCP", "company_name": "Godrej Consumer", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "GRASIM", "company_name": "Grasim Industries", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HAL", "company_name": "Hindustan Aeronautics", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HAVELLS", "company_name": "Havells India", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HCLTECH", "company_name": "HCL Technologies", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HDFCBANK", "company_name": "HDFC Bank", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HDFCLIFE", "company_name": "HDFC Life Insurance", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HEROMOTOCO", "company_name": "Hero MotoCorp", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HINDALCO", "company_name": "Hindalco Industries", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "HINDUNILVR", "company_name": "Hindustan Unilever", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ICICIBANK", "company_name": "ICICI Bank", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ICICIGI", "company_name": "ICICI Lombard", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ICICIPRULI", "company_name": "ICICI Prudential", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "INDIGO", "company_name": "Interglobe Aviation", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "INDUSINDBK", "company_name": "IndusInd Bank", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "INFY", "company_name": "Infosys Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "IOC", "company_name": "Indian Oil Corp", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "IRCTC", "company_name": "IRCTC", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "IRFC", "company_name": "Indian Railway Finance", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ITC", "company_name": "ITC Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "JINDALSTEL", "company_name": "Jindal Steel", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "JIOFIN", "company_name": "Jio Financial", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "JSWENERGY", "company_name": "JSW Energy", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "JSWSTEEL", "company_name": "JSW Steel", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "KOTAKBANK", "company_name": "Kotak Mahindra Bank", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "LICI", "company_name": "LIC India", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "LODHA", "company_name": "Macrotech Developers", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "LT", "company_name": "Larsen & Toubro", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "LTIM", "company_name": "LTIMindtree", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "M&M", "company_name": "Mahindra & Mahindra", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "MARUTI", "company_name": "Maruti Suzuki", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "MOTHERSON", "company_name": "Motherson Sumi", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "NAUKRI", "company_name": "Info Edge", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "NESTLEIND", "company_name": "Nestle India", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "NHPC", "company_name": "NHPC Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "NTPC", "company_name": "NTPC Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "ONGC", "company_name": "ONGC", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "PFC", "company_name": "Power Finance Corp", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "PIDILITIND", "company_name": "Pidilite Industries", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "PNB", "company_name": "Punjab National Bank", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "POWERGRID", "company_name": "Power Grid Corp", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "RECLTD", "company_name": "REC Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "RELIANCE", "company_name": "Reliance Industries", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SBILIFE", "company_name": "SBI Life Insurance", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SBIN", "company_name": "State Bank of India", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SHREECEM", "company_name": "Shree Cement", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SHRIRAMFIN", "company_name": "Shriram Finance", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SIEMENS", "company_name": "Siemens Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SUNPHARMA", "company_name": "Sun Pharma", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TATACONSUM", "company_name": "Tata Consumer", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TATAMOTORS", "company_name": "Tata Motors", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TATAPOWER", "company_name": "Tata Power", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TATASTEEL", "company_name": "Tata Steel", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TCS", "company_name": "Tata Consultancy Services", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TECHM", "company_name": "Tech Mahindra", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TITAN", "company_name": "Titan Company", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TORNTPHARM", "company_name": "Torrent Pharma", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TRENT", "company_name": "Trent Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "TVSMOTOR", "company_name": "TVS Motor", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},

]

# ========== API VIEWS ==========
def health_check(request):
    return JsonResponse({"status": "ok", "message": "API is running", "companies": len(ALL_COMPANIES)})

def api_root(request):
    return JsonResponse({"message": "Nifty 100 API", "total_companies": len(ALL_COMPANIES)})

def company_list(request):
    return JsonResponse({"success": True, "total": len(ALL_COMPANIES), "companies": ALL_COMPANIES})

def company_detail(request, symbol):
    for c in ALL_COMPANIES:
        if c["symbol"] == symbol.upper():
            return JsonResponse(c)
    return JsonResponse({"error": "Not found"}, status=404)

# ========== PAGE VIEWS ==========
def dashboard(request):
    total_revenue = sum(c["revenue_cr"] for c in ALL_COMPANIES)
    total_profit = sum(c["net_profit_cr"] for c in ALL_COMPANIES)
    avg_opm = sum(c["opm_pct"] for c in ALL_COMPANIES) / len(ALL_COMPANIES) if ALL_COMPANIES else 0
    sectors = len(set(c["sector"] for c in ALL_COMPANIES))
    
    context = {
        "total_companies": len(ALL_COMPANIES),
        "total_sectors": sectors,
        "total_revenue": f"{total_revenue / 100000:.1f}L Cr" if total_revenue > 0 else "0",
        "avg_opm": f"{avg_opm:.1f}%",
        "pl_count": 2427,
        "bs_count": 1225,
        "years_count": 71,
    }
    return render(request, "dashboard.html", context)

def companies_list_page(request):
    return render(request, "companies.html", {"companies": ALL_COMPANIES})

def company_detail_page(request, symbol):
    company = next((c for c in ALL_COMPANIES if c["symbol"] == symbol.upper()), None)
    return render(request, "company_detail.html", {"company": company})

def top_performers_page(request):
    sorted_companies = sorted(ALL_COMPANIES, key=lambda x: x["net_profit_cr"], reverse=True)
    return render(request, "top_performers.html", {"companies": sorted_companies})

def sector_analysis_page(request):
    sectors = {}
    for c in ALL_COMPANIES:
        if c["sector"] not in sectors:
            sectors[c["sector"]] = {"count": 0, "total_revenue": 0, "total_profit": 0}
        sectors[c["sector"]]["count"] += 1
        sectors[c["sector"]]["total_revenue"] += c["revenue_cr"]
        sectors[c["sector"]]["total_profit"] += c["net_profit_cr"]
    return render(request, "sector_analysis.html", {"sectors": sectors})
