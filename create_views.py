# This script combines your company list with financial data
import pandas as pd

# Read financial data from Excel
df_pl = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=1)

# Create a dictionary of financial data by company
financial_data = {}
for _, row in df_pl.iterrows():
    symbol = str(row.get('company_id', '')).strip()
    if symbol and symbol != 'nan':
        year_str = str(row.get('year', ''))
        if '2024' in year_str and 'TTM' not in year_str:
            financial_data[symbol] = {
                'revenue_cr': float(row.get('sales', 0)) if pd.notna(row.get('sales')) else 0,
                'net_profit_cr': float(row.get('net_profit', 0)) if pd.notna(row.get('net_profit')) else 0,
                'opm_pct': float(row.get('opm_percentage', 0)) if pd.notna(row.get('opm_percentage')) else 0,
            }
            break

# List of all companies (from your output)
companies = [
    ("ABB", "Abbott India Ltd"),
    ("ADANIENSOL", "Adani Energy Solutions Ltd"),
    ("ADANIENT", "Adani Enterprises Ltd"),
    ("ADANIGREEN", "Adani Green Energy Ltd"),
    ("ADANIPORTS", "Adani Ports"),
    ("ADANIPOWER", "Adani Power Ltd"),
    ("AMBUJACEM", "Ambuja Cements Ltd"),
    ("APOLLOHOSP", "Apollo Hospitals"),
    ("ASIANPAINT", "Asian Paints"),
    ("ATGL", "Adani Total Gas Ltd"),
    ("AXISBANK", "Axis Bank Ltd"),
    ("BAJAJ-AUTO", "Bajaj Auto Ltd"),
    ("BAJAJFINSV", "Bajaj Finserv Ltd"),
    ("BAJAJHLDNG", "Bajaj Holdings"),
    ("BAJFINANCE", "Bajaj Finance Ltd"),
    ("BANKBARODA", "Bank of Baroda"),
    ("BEL", "Bharat Electronics Ltd"),
    ("BHARTIARTL", "Bharti Airtel Ltd"),
    ("BHEL", "Bharat Heavy Electricals"),
    ("BOSCHLTD", "Bosch Ltd"),
    ("BPCL", "Bharat Petroleum Corp"),
    ("BRITANNIA", "Britannia Industries"),
    ("CANBK", "Canara Bank"),
    ("CHOLAFIN", "Cholamandalam Investment"),
    ("CIPLA", "Cipla Ltd"),
    ("COALINDIA", "Coal India Ltd"),
    ("DABUR", "Dabur India Ltd"),
    ("DIVISLAB", "Divis Laboratories"),
    ("DLF", "DLF Ltd"),
    ("DMART", "Avenue Supermarts"),
    ("DRREDDY", "Dr Reddys Labs"),
    ("EICHERMOT", "Eicher Motors"),
    ("GAIL", "GAIL India"),
    ("GODREJCP", "Godrej Consumer"),
    ("GRASIM", "Grasim Industries"),
    ("HAL", "Hindustan Aeronautics"),
    ("HAVELLS", "Havells India"),
    ("HCLTECH", "HCL Technologies"),
    ("HDFCBANK", "HDFC Bank"),
    ("HDFCLIFE", "HDFC Life Insurance"),
    ("HEROMOTOCO", "Hero MotoCorp"),
    ("HINDALCO", "Hindalco Industries"),
    ("HINDUNILVR", "Hindustan Unilever"),
    ("ICICIBANK", "ICICI Bank"),
    ("ICICIGI", "ICICI Lombard"),
    ("ICICIPRULI", "ICICI Prudential"),
    ("INDIGO", "Interglobe Aviation"),
    ("INDUSINDBK", "IndusInd Bank"),
    ("INFY", "Infosys Ltd"),
    ("IOC", "Indian Oil Corp"),
    ("IRCTC", "IRCTC"),
    ("IRFC", "Indian Railway Finance"),
    ("ITC", "ITC Ltd"),
    ("JINDALSTEL", "Jindal Steel"),
    ("JIOFIN", "Jio Financial"),
    ("JSWENERGY", "JSW Energy"),
    ("JSWSTEEL", "JSW Steel"),
    ("KOTAKBANK", "Kotak Mahindra Bank"),
    ("LICI", "LIC India"),
    ("LODHA", "Macrotech Developers"),
    ("LT", "Larsen & Toubro"),
    ("LTIM", "LTIMindtree"),
    ("M&M", "Mahindra & Mahindra"),
    ("MARUTI", "Maruti Suzuki"),
    ("MOTHERSON", "Motherson Sumi"),
    ("NAUKRI", "Info Edge"),
    ("NESTLEIND", "Nestle India"),
    ("NHPC", "NHPC Ltd"),
    ("NTPC", "NTPC Ltd"),
    ("ONGC", "ONGC"),
    ("PFC", "Power Finance Corp"),
    ("PIDILITIND", "Pidilite Industries"),
    ("PNB", "Punjab National Bank"),
    ("POWERGRID", "Power Grid Corp"),
    ("RECLTD", "REC Ltd"),
    ("RELIANCE", "Reliance Industries"),
    ("SBILIFE", "SBI Life Insurance"),
    ("SBIN", "State Bank of India"),
    ("SHREECEM", "Shree Cement"),
    ("SHRIRAMFIN", "Shriram Finance"),
    ("SIEMENS", "Siemens Ltd"),
    ("SUNPHARMA", "Sun Pharma"),
    ("TATACONSUM", "Tata Consumer"),
    ("TATAMOTORS", "Tata Motors"),
    ("TATAPOWER", "Tata Power"),
    ("TATASTEEL", "Tata Steel"),
    ("TCS", "Tata Consultancy Services"),
    ("TECHM", "Tech Mahindra"),
    ("TITAN", "Titan Company"),
    ("TORNTPHARM", "Torrent Pharma"),
    ("TRENT", "Trent Ltd"),
    ("TVSMOTOR", "TVS Motor"),
]

# Generate the views.py content
output = '''from django.http import JsonResponse
from django.shortcuts import render

# ========== ALL 92 NIFTY COMPANIES WITH FINANCIAL DATA ==========
ALL_COMPANIES = [
'''

for symbol, name in companies:
    fin = financial_data.get(symbol, {'revenue_cr': 0, 'net_profit_cr': 0, 'opm_pct': 0})
    output += f'    {{"symbol": "{symbol}", "company_name": "{name}", "sector": "Other", "revenue_cr": {fin["revenue_cr"]}, "net_profit_cr": {fin["net_profit_cr"]}, "opm_pct": {fin["opm_pct"]}}},\n'

output += '''
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
'''

# Write the file
with open('nifty_api/views.py', 'w', encoding='utf-8') as f:
    f.write(output)

print("✅ views.py created with all 92 companies!")
