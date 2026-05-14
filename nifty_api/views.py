from django.http import JsonResponse
from django.shortcuts import render

# ========== HARDCODED DATA FROM EXCEL ==========
ALL_COMPANIES = [
    {"symbol": "ABB", "company_name": "Abbott India Ltd", "sector": "Other", "revenue_cr": 5849.0, "net_profit_cr": 1201.0, "opm_pct": 25.0},
    {"symbol": "ADANIENSOL", "company_name": "Adani Energy Solutions Ltd", "sector": "Energy", "revenue_cr": 16607.0, "net_profit_cr": 1196.0, "opm_pct": 30.0},
    {"symbol": "ADANIENT", "company_name": "Adani Enterprises Ltd", "sector": "Energy", "revenue_cr": 96421.0, "net_profit_cr": 3335.0, "opm_pct": 12.0},
    {"symbol": "ADANIGREEN", "company_name": "Adani Green Energy Ltd", "sector": "Energy", "revenue_cr": 9220.0, "net_profit_cr": 1260.0, "opm_pct": 79.0},
    {"symbol": "ADANIPORTS", "company_name": "Adani Ports & Special Economic Zone Ltd ", "sector": "Energy", "revenue_cr": 26711.0, "net_profit_cr": 8104.0, "opm_pct": 58.0},
    {"symbol": "ADANIPOWER", "company_name": "Adani Power Ltd", "sector": "Energy", "revenue_cr": 50351.0, "net_profit_cr": 20829.0, "opm_pct": 36.0},
    {"symbol": "AMBUJACEM", "company_name": "Ambuja Cements Ltd", "sector": "Other", "revenue_cr": 33160.0, "net_profit_cr": 4738.0, "opm_pct": 19.0},
    {"symbol": "APOLLOHOSP", "company_name": "Apollo Hospitals Chain of Indian private hospitals", "sector": "Other", "revenue_cr": 19059.0, "net_profit_cr": 935.0, "opm_pct": 13.0},
    {"symbol": "ASIANPAINT", "company_name": "Asian Paints Indian Multi-National Paint and Coating Manufacturing Company", "sector": "Other", "revenue_cr": 35495.0, "net_profit_cr": 5558.0, "opm_pct": 21.0},
    {"symbol": "ATGL", "company_name": "Adani Total Gas Ltd", "sector": "Energy", "revenue_cr": 4475.0, "net_profit_cr": 668.0, "opm_pct": 25.0},
    {"symbol": "AXISBANK", "company_name": "Axis Bank Ltd", "sector": "Banking", "revenue_cr": 109369.0, "net_profit_cr": 24861.0, "opm_pct": 11952.0},
    {"symbol": "BAJAJ-AUTO", "company_name": "Bajaj Auto Ltd", "sector": "Auto", "revenue_cr": 44870.0, "net_profit_cr": 7708.0, "opm_pct": 20.0},
    {"symbol": "BAJAJFINSV", "company_name": "Bajaj Finserv Ltd", "sector": "Financial Services", "revenue_cr": 110382.0, "net_profit_cr": 15595.0, "opm_pct": 37.0},
    {"symbol": "BAJAJHLDNG", "company_name": "Bajaj Holdings & Investment Ltd", "sector": "Other", "revenue_cr": 1702.0, "net_profit_cr": 7365.0, "opm_pct": 92.0},
    {"symbol": "BAJFINANCE", "company_name": "Bajaj Finance Ltd", "sector": "Financial Services", "revenue_cr": 54972.0, "net_profit_cr": 14451.0, "opm_pct": 19987.0},
    {"symbol": "BANKBARODA", "company_name": "Bank of Baroda", "sector": "Banking", "revenue_cr": 118379.0, "net_profit_cr": 18869.0, "opm_pct": 4102.0},
    {"symbol": "BEL", "company_name": "Bharat Electronics Ltd", "sector": "Other", "revenue_cr": 20268.0, "net_profit_cr": 3985.0, "opm_pct": 25.0},
    {"symbol": "BHARTIARTL", "company_name": "Bharti Airtel Ltd", "sector": "Other", "revenue_cr": 149982.0, "net_profit_cr": 8558.0, "opm_pct": 52.0},
    {"symbol": "BHEL", "company_name": "Bharat Heavy Electricals Limited ", "sector": "Other", "revenue_cr": 23893.0, "net_profit_cr": 282.0, "opm_pct": 3.0},
    {"symbol": "BOSCHLTD", "company_name": "Bosch Ltd", "sector": "Other", "revenue_cr": 16727.0, "net_profit_cr": 2490.0, "opm_pct": 13.0},
    {"symbol": "BPCL", "company_name": "Bharat Petroleum Corporation Ltd", "sector": "Other", "revenue_cr": 448083.0, "net_profit_cr": 26859.0, "opm_pct": 10.0},
    {"symbol": "BRITANNIA", "company_name": "Britannia Industries Ltd", "sector": "FMCG", "revenue_cr": 16769.0, "net_profit_cr": 2134.0, "opm_pct": 19.0},
    {"symbol": "CANBK", "company_name": "Canara Bank", "sector": "Banking", "revenue_cr": 110519.0, "net_profit_cr": 15401.0, "opm_pct": -7745.0},
    {"symbol": "CHOLAFIN", "company_name": "Cholamandalam Investment & Finance Company Ltd", "sector": "Financial Services", "revenue_cr": 19163.0, "net_profit_cr": 3420.0, "opm_pct": 4548.0},
    {"symbol": "CIPLA", "company_name": "Cipla Ltd ", "sector": "Pharma", "revenue_cr": 25774.0, "net_profit_cr": 4154.0, "opm_pct": 6291.0},
    {"symbol": "COALINDIA", "company_name": "Coal India Ltd", "sector": "Other", "revenue_cr": 142324.0, "net_profit_cr": 37369.0, "opm_pct": 47971.0},
    {"symbol": "DABUR", "company_name": "Dabur India Ltd", "sector": "FMCG", "revenue_cr": 12404.0, "net_profit_cr": 1811.0, "opm_pct": 19.0},
    {"symbol": "DIVISLAB", "company_name": "Divis Laboratories Ltd", "sector": "Pharma", "revenue_cr": 7845.0, "net_profit_cr": 1600.0, "opm_pct": 28.0},
    {"symbol": "DLF", "company_name": "DLF Ltd", "sector": "Other", "revenue_cr": 6427.0, "net_profit_cr": 2724.0, "opm_pct": 33.0},
    {"symbol": "DMART", "company_name": "Avenue Supermarts Ltd", "sector": "Other", "revenue_cr": 50789.0, "net_profit_cr": 2536.0, "opm_pct": 8.0},
    {"symbol": "DRREDDY", "company_name": "Dr Reddys Laboratories Ltd", "sector": "Other", "revenue_cr": 28011.0, "net_profit_cr": 5578.0, "opm_pct": 28.0},
    {"symbol": "EICHERMOT", "company_name": "Eicher Motors Ltd", "sector": "Auto", "revenue_cr": 16536.0, "net_profit_cr": 4001.0, "opm_pct": 26.0},
    {"symbol": "GAIL", "company_name": "GAIL (India) Ltd", "sector": "Other", "revenue_cr": 133228.0, "net_profit_cr": 9903.0, "opm_pct": 11.0},
    {"symbol": "GODREJCP", "company_name": "Godrej Consumer Products Ltd", "sector": "FMCG", "revenue_cr": 14096.0, "net_profit_cr": -561.0, "opm_pct": 21.0},
    {"symbol": "GRASIM", "company_name": "Grasim Industries Ltd", "sector": "Other", "revenue_cr": 130978.0, "net_profit_cr": 9926.0, "opm_pct": 21.0},
    {"symbol": "HAL", "company_name": "Hindustan Aeronautics Ltd", "sector": "Other", "revenue_cr": 30381.0, "net_profit_cr": 7595.0, "opm_pct": 32.0},
    {"symbol": "HAVELLS", "company_name": "Havells India Ltd", "sector": "Other", "revenue_cr": 18590.0, "net_profit_cr": 1271.0, "opm_pct": 10.0},
    {"symbol": "HCLTECH", "company_name": "HCL Technologies Ltd", "sector": "IT", "revenue_cr": 109913.0, "net_profit_cr": 15710.0, "opm_pct": 22.0},
    {"symbol": "HDFCBANK", "company_name": "HDFC Bank Ltd", "sector": "Banking", "revenue_cr": 283649.0, "net_profit_cr": 65446.0, "opm_pct": -44685.0},
    {"symbol": "HDFCLIFE", "company_name": "HDFC Life Insurance Company Ltd", "sector": "Banking", "revenue_cr": 101482.0, "net_profit_cr": 1574.0, "opm_pct": 531.0},
    {"symbol": "HEROMOTOCO", "company_name": "Hero MotoCorp Ltd ", "sector": "Auto", "revenue_cr": 37789.0, "net_profit_cr": 3742.0, "opm_pct": 5235.0},
    {"symbol": "HINDALCO", "company_name": "Hindalco Industries Ltd", "sector": "Other", "revenue_cr": 215962.0, "net_profit_cr": 10155.0, "opm_pct": 23872.0},
    {"symbol": "HINDUNILVR", "company_name": "Hindustan Unilever Ltd ", "sector": "FMCG", "revenue_cr": 61896.0, "net_profit_cr": 10282.0, "opm_pct": 14659.0},
    {"symbol": "ICICIBANK", "company_name": "ICICI Bank Ltd", "sector": "Banking", "revenue_cr": 159516.0, "net_profit_cr": 46081.0, "opm_pct": -14152.0},
    {"symbol": "ICICIGI", "company_name": "ICICI Lombard General Insurance Company Ltd", "sector": "Banking", "revenue_cr": 20487.0, "net_profit_cr": 1919.0, "opm_pct": 2577.0},
    {"symbol": "ICICIPRULI", "company_name": "ICICI Prudential Life Insurance Company Ltd", "sector": "Banking", "revenue_cr": 90307.0, "net_profit_cr": 851.0, "opm_pct": -1829.0},
    {"symbol": "INDIGO", "company_name": "Interglobe Aviation Ltd", "sector": "Other", "revenue_cr": 68904.0, "net_profit_cr": 8167.0, "opm_pct": 16331.0},
    {"symbol": "INDUSINDBK", "company_name": "IndusInd Bank Ltd", "sector": "Banking", "revenue_cr": 45748.0, "net_profit_cr": 8950.0, "opm_pct": 2978.0},
    {"symbol": "INFY", "company_name": "Infosys Ltd", "sector": "IT", "revenue_cr": 153670.0, "net_profit_cr": 26248.0, "opm_pct": 24.0},
    {"symbol": "IOC", "company_name": "Indian Oil Corporation ", "sector": "Energy", "revenue_cr": 776352.0, "net_profit_cr": 43161.0, "opm_pct": 10.0},
    {"symbol": "IRCTC", "company_name": "Indian Railway Catering & Tourism Corporation Ltd", "sector": "Other", "revenue_cr": 4270.0, "net_profit_cr": 1111.0, "opm_pct": 34.0},
    {"symbol": "IRFC", "company_name": "Indian Railway Finance Corporation Ltd", "sector": "Financial Services", "revenue_cr": 26645.0, "net_profit_cr": 6412.0, "opm_pct": 100.0},
    {"symbol": "ITC", "company_name": "ITC Ltd ", "sector": "FMCG", "revenue_cr": 70866.0, "net_profit_cr": 20751.0, "opm_pct": 37.0},
    {"symbol": "JINDALSTEL", "company_name": "Jindal Steel & Power Ltd", "sector": "Energy", "revenue_cr": 50354.0, "net_profit_cr": 5943.0, "opm_pct": 20.0},
    {"symbol": "JIOFIN", "company_name": "Jio Financial Services Ltd", "sector": "Other", "revenue_cr": 1855.0, "net_profit_cr": 1605.0, "opm_pct": 84.0},
    {"symbol": "JSWENERGY", "company_name": "JSW Energy Ltd", "sector": "Other", "revenue_cr": 11486.0, "net_profit_cr": 1725.0, "opm_pct": 47.0},
    {"symbol": "JSWSTEEL", "company_name": "JSW Steel Ltd", "sector": "Other", "revenue_cr": 175006.0, "net_profit_cr": 8973.0, "opm_pct": 16.0},
    {"symbol": "KOTAKBANK", "company_name": "Kotak Mahindra Bank Ltd ", "sector": "Banking", "revenue_cr": 56237.0, "net_profit_cr": 18213.0, "opm_pct": -13382.0},
    {"symbol": "LICI", "company_name": "Life Insurance Corporation of India", "sector": "Other", "revenue_cr": 845966.0, "net_profit_cr": 40916.0, "opm_pct": 4.0},
    {"symbol": "LODHA", "company_name": "Macrotech Developers Ltd", "sector": "IT", "revenue_cr": 10316.0, "net_profit_cr": 1554.0, "opm_pct": 26.0},
    {"symbol": "LT", "company_name": "Larsen & Toubro Ltd", "sector": "Other", "revenue_cr": 221113.0, "net_profit_cr": 15547.0, "opm_pct": 14.0},
    {"symbol": "LTIM", "company_name": "LTIMindtree Ltd", "sector": "IT", "revenue_cr": 35517.0, "net_profit_cr": 4585.0, "opm_pct": 18.0},
    {"symbol": "M&M", "company_name": "Mahindra & Mahindra Ltd ", "sector": "Auto", "revenue_cr": 139078.0, "net_profit_cr": 12270.0, "opm_pct": 18.0},
    {"symbol": "MARUTI", "company_name": "Maruti Suzuki India Ltd", "sector": "Auto", "revenue_cr": 141858.0, "net_profit_cr": 13488.0, "opm_pct": 13.0},
    {"symbol": "MOTHERSON", "company_name": "Samvardhana Motherson International Ltd", "sector": "Other", "revenue_cr": 98692.0, "net_profit_cr": 3020.0, "opm_pct": 9.0},
    {"symbol": "NAUKRI", "company_name": "Info Edge (India) Ltd", "sector": "Other", "revenue_cr": 2536.0, "net_profit_cr": 595.0, "opm_pct": 28.0},
    {"symbol": "NESTLEIND", "company_name": "Nestle India Ltd", "sector": "FMCG", "revenue_cr": 24394.0, "net_profit_cr": 3933.0, "opm_pct": 24.0},
    {"symbol": "NHPC", "company_name": "NHPC Ltd ", "sector": "Other", "revenue_cr": 9632.0, "net_profit_cr": 4028.0, "opm_pct": 50.0},
    {"symbol": "NTPC", "company_name": "NTPC Ltd", "sector": "Energy", "revenue_cr": 178501.0, "net_profit_cr": 21332.0, "opm_pct": 29.0},
    {"symbol": "ONGC", "company_name": "Oil & Natural Gas Corpn Ltd", "sector": "Energy", "revenue_cr": 591396.0, "net_profit_cr": 57101.0, "opm_pct": 17.0},
    {"symbol": "PFC", "company_name": "Power Finance Corporation Ltd", "sector": "Energy", "revenue_cr": 91508.0, "net_profit_cr": 26461.0, "opm_pct": 37.0},
    {"symbol": "PIDILITIND", "company_name": "Pidilite Industries Ltd", "sector": "Other", "revenue_cr": 12383.0, "net_profit_cr": 1747.0, "opm_pct": 22.0},
    {"symbol": "PNB", "company_name": "Punjab National Bank", "sector": "Banking", "revenue_cr": 109065.0, "net_profit_cr": 9157.0, "opm_pct": 0},
    {"symbol": "POWERGRID", "company_name": "Power Grid Corporation of India Ltd", "sector": "Energy", "revenue_cr": 45843.0, "net_profit_cr": 15573.0, "opm_pct": 87.0},
    {"symbol": "RECLTD", "company_name": "REC Ltd", "sector": "Other", "revenue_cr": 47517.0, "net_profit_cr": 14145.0, "opm_pct": 101.0},
    {"symbol": "RELIANCE", "company_name": "Reliance Industries Ltd ", "sector": "Energy", "revenue_cr": 899041.0, "net_profit_cr": 79020.0, "opm_pct": 18.0},
    {"symbol": "SBILIFE", "company_name": "SBI Life Insurance Company Ltd", "sector": "Banking", "revenue_cr": 131988.0, "net_profit_cr": 1894.0, "opm_pct": 0.0},
    {"symbol": "SBIN", "company_name": "State Bank of India", "sector": "Banking", "revenue_cr": 439189.0, "net_profit_cr": 69543.0, "opm_pct": -14.0},
    {"symbol": "SHREECEM", "company_name": "Shree Cement Ltd", "sector": "Other", "revenue_cr": 20521.0, "net_profit_cr": 1733.0, "opm_pct": 22.0},
    {"symbol": "SHRIRAMFIN", "company_name": "Shriram Finance Ltd ", "sector": "Financial Services", "revenue_cr": 36388.0, "net_profit_cr": 7399.0, "opm_pct": 29.0},
    {"symbol": "SIEMENS", "company_name": "Siemens Ltd", "sector": "Other", "revenue_cr": 0, "net_profit_cr": 0, "opm_pct": 0},
    {"symbol": "SUNPHARMA", "company_name": "Sun Pharmaceuticals Industries Ltd", "sector": "Pharma", "revenue_cr": 48497.0, "net_profit_cr": 9610.0, "opm_pct": 28.0},
    {"symbol": "TATACONSUM", "company_name": "Tata Consumer Products Ltd", "sector": "FMCG", "revenue_cr": 15206.0, "net_profit_cr": 1215.0, "opm_pct": 15.0},
    {"symbol": "TATAMOTORS", "company_name": "Tata Motors Ltd", "sector": "Auto", "revenue_cr": 437928.0, "net_profit_cr": 31807.0, "opm_pct": 14.0},
    {"symbol": "TATAPOWER", "company_name": "Tata Power Company Ltd ", "sector": "Energy", "revenue_cr": 61449.0, "net_profit_cr": 4280.0, "opm_pct": 17.0},
    {"symbol": "TATASTEEL", "company_name": "Tata Steel Ltd ", "sector": "Other", "revenue_cr": 229171.0, "net_profit_cr": -4910.0, "opm_pct": 10.0},
    {"symbol": "TCS", "company_name": "Tata Consultancy Services Ltd", "sector": "Other", "revenue_cr": 240893.0, "net_profit_cr": 46099.0, "opm_pct": 27.0},
    {"symbol": "TECHM", "company_name": "Tech Mahindra Ltd", "sector": "IT", "revenue_cr": 51996.0, "net_profit_cr": 2397.0, "opm_pct": 9.0},
    {"symbol": "TITAN", "company_name": "Titan Company Ltd ", "sector": "Other", "revenue_cr": 51084.0, "net_profit_cr": 3496.0, "opm_pct": 10.0},
    {"symbol": "TORNTPHARM", "company_name": "Torrent Pharmaceuticals Ltd", "sector": "Pharma", "revenue_cr": 10728.0, "net_profit_cr": 1656.0, "opm_pct": 31.0},
    {"symbol": "TRENT", "company_name": "Trent Ltd", "sector": "Other", "revenue_cr": 12375.0, "net_profit_cr": 1477.0, "opm_pct": 16.0},
    {"symbol": "TVSMOTOR", "company_name": "TVS Motor Company Ltd", "sector": "Auto", "revenue_cr": 39145.0, "net_profit_cr": 1779.0, "opm_pct": 14.0},

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
    sorted_companies = sorted(ALL_COMPANIES, key=lambda x: x["net_profit_cr"], reverse=True)[:20]
    result = []
    for idx, c in enumerate(sorted_companies, 1):
        result.append({"rank": idx, "symbol": c["symbol"], "company_name": c["company_name"], "sector": c["sector"], "net_profit_cr": c["net_profit_cr"]})
    return JsonResponse({"top_performers": result})

def sector_analysis(request):
    sectors = {}
    for c in ALL_COMPANIES:
        if c["sector"] not in sectors:
            sectors[c["sector"]] = {"count": 0, "total_revenue": 0, "total_profit": 0, "total_opm": 0}
        sectors[c["sector"]]["count"] += 1
        sectors[c["sector"]]["total_revenue"] += c["revenue_cr"]
        sectors[c["sector"]]["total_profit"] += c["net_profit_cr"]
        sectors[c["sector"]]["total_opm"] += c["opm_pct"]
    
    result = []
    for sector, data in sectors.items():
        result.append({
            "sector": sector,
            "companies": data["count"],
            "total_revenue_cr": data["total_revenue"],
            "total_profit_cr": data["total_profit"],
            "avg_opm_pct": data["total_opm"] / data["count"] if data["count"] > 0 else 0
        })
    result.sort(key=lambda x: x["total_profit_cr"], reverse=True)
    return JsonResponse({"sectors": result})

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
