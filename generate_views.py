import pandas as pd
import json

print("=" * 60)
print("📊 Generating views.py from Excel data")
print("=" * 60)

# Read all data
df_companies = pd.read_excel('companies.xlsx', sheet_name='Companies', header=1)
df_pl = pd.read_excel('profitandloss.xlsx', sheet_name='Profit & Loss', header=1)
df_bs = pd.read_excel('balancesheet.xlsx', sheet_name='Balance Sheet', header=1)

print(f"✅ Companies: {len(df_companies)}")
print(f"✅ P&L Records: {len(df_pl)}")
print(f"✅ Balance Sheet Records: {len(df_bs)}")

# Extract companies with their latest financial data
companies_list = []
for _, row in df_companies.iterrows():
    symbol = str(row.get('id', '')).strip()
    if not symbol or symbol == 'nan' or symbol == '':
        continue
    
    name = str(row.get('company_name', ''))[:80].replace('"', '\\"').replace('\n', ' ')
    sector = "Other"
    
    # Try to get sector from name
    name_lower = name.lower()
    if any(word in name_lower for word in ['bank', 'hdfc', 'sbi', 'icici', 'axis', 'kotak', 'indusind', 'pnb', 'canara', 'baroda']):
        sector = "Banking"
    elif any(word in name_lower for word in ['tech', 'tcs', 'infosys', 'wipro', 'hcl', 'techm', 'ltim']):
        sector = "IT"
    elif any(word in name_lower for word in ['reliance', 'ongc', 'oil', 'gas', 'power', 'adani', 'ntpc']):
        sector = "Energy"
    elif any(word in name_lower for word in ['auto', 'motor', 'maruti', 'bajaj auto', 'hero', 'eicher', 'mahindra', 'tata motors']):
        sector = "Auto"
    elif any(word in name_lower for word in ['pharma', 'sun', 'dr.reddy', 'cipla', 'divis']):
        sector = "Pharma"
    elif any(word in name_lower for word in ['consumer', 'unilever', 'itc', 'dabur', 'nestle', 'britannia']):
        sector = "FMCG"
    elif any(word in name_lower for word in ['finance', 'bajaj finance', 'bajaj finserv', 'lic']):
        sector = "Financial Services"
    
    # Get latest financial data for 2024
    pl_data = df_pl[df_pl['company_id'] == symbol]
    pl_2024 = pl_data[pl_data['year'].astype(str).str.contains('Mar 2024', na=False)]
    
    revenue = 0
    profit = 0
    opm = 0
    
    if not pl_2024.empty:
        revenue = float(pl_2024.iloc[0]['sales']) if pd.notna(pl_2024.iloc[0]['sales']) else 0
        profit = float(pl_2024.iloc[0]['net_profit']) if pd.notna(pl_2024.iloc[0]['net_profit']) else 0
        opm = float(pl_2024.iloc[0]['opm_percentage']) if pd.notna(pl_2024.iloc[0]['opm_percentage']) else 0
    
    companies_list.append({
        'symbol': symbol,
        'name': name,
        'sector': sector,
        'revenue': revenue,
        'profit': profit,
        'opm': opm
    })

print(f"✅ Processed {len(companies_list)} companies")

# Generate views.py
output = '''from django.http import JsonResponse
from django.shortcuts import render

# ========== HARDCODED DATA FROM EXCEL ==========
ALL_COMPANIES = [
'''

for c in companies_list:
    output += f'    {{"symbol": "{c["symbol"]}", "company_name": "{c["name"]}", "sector": "{c["sector"]}", "revenue_cr": {c["revenue"]}, "net_profit_cr": {c["profit"]}, "opm_pct": {c["opm"]}}},\n'

output += '''
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
'''

with open('nifty_api/views.py', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"\n✅ views.py generated with {len(companies_list)} companies!")
print("=" * 60)
