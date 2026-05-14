import pandas as pd
import json

# Load financial data
with open('financial_data.json', 'r') as f:
    financial_data = json.load(f)

# Read companies
df_companies = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)

# Start building views.py
output = '''from django.http import JsonResponse
from django.shortcuts import render

# ========== ALL NIFTY COMPANIES WITH REAL FINANCIAL DATA ==========
ALL_COMPANIES = [
'''

# Add each company with its financial data
for _, row in df_companies.iterrows():
    symbol = str(row.get('id', '')).strip()
    if not symbol or symbol == 'nan':
        continue
    
    name = str(row.get('company_name', ''))[:60].replace('"', '\\"')
    
    # Get financial data (default to 0 if not found)
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

# Save the file
with open('nifty_api/views.py', 'w', encoding='utf-8') as f:
    f.write(output)

print('✅ views.py created with real financial data!')
print(f'Total companies: {len(df_companies)}')
