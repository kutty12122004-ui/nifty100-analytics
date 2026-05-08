# nifty_api/views.py - Complete working version
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# ============================================================
# API ENDPOINTS
# ============================================================

@csrf_exempt
def health_check(request):
    """API health check endpoint"""
    return JsonResponse({
        "message": "Nifty 100 API is live and connected!",
        "status": "active",
        "database": "Sample Data Mode",
        "version": "1.0.0"
    })

@csrf_exempt
def api_root(request):
    """Root API endpoint with all available endpoints"""
    return JsonResponse({
        "message": "Nifty 100 Financial Intelligence API",
        "version": "1.0.0",
        "status": "Fully Operational",
        "endpoints": {
            "health": "/api/health/",
            "companies": "/api/companies/",
            "company_detail": "/api/companies/{symbol}/",
            "company_financials": "/api/companies/{symbol}/financials/",
            "top_performers": "/api/top-performers/",
            "sector_analysis": "/api/sector-analysis/",
        }
    })

@csrf_exempt
def company_list(request):
    """Get all companies - Nifty 100 companies"""
    companies = [
        {"symbol": "TCS", "company_name": "Tata Consultancy Services", "sector": "IT", "face_value": 1, "book_value": 250, "revenue_cr": 240000, "net_profit_cr": 45000, "opm_pct": 25.5},
        {"symbol": "INFY", "company_name": "Infosys Limited", "sector": "IT", "face_value": 5, "book_value": 180, "revenue_cr": 150000, "net_profit_cr": 28000, "opm_pct": 24.5},
        {"symbol": "WIPRO", "company_name": "Wipro Limited", "sector": "IT", "face_value": 2, "book_value": 120, "revenue_cr": 90000, "net_profit_cr": 15000, "opm_pct": 22.0},
        {"symbol": "HCLTECH", "company_name": "HCL Technologies", "sector": "IT", "face_value": 2, "book_value": 150, "revenue_cr": 120000, "net_profit_cr": 22000, "opm_pct": 23.0},
        {"symbol": "HDFCBANK", "company_name": "HDFC Bank", "sector": "Banking", "face_value": 1, "book_value": 450, "revenue_cr": 180000, "net_profit_cr": 35000, "opm_pct": 20.5},
        {"symbol": "ICICIBANK", "company_name": "ICICI Bank", "sector": "Banking", "face_value": 2, "book_value": 300, "revenue_cr": 150000, "net_profit_cr": 32000, "opm_pct": 18.5},
        {"symbol": "SBIN", "company_name": "State Bank of India", "sector": "Banking", "face_value": 1, "book_value": 280, "revenue_cr": 400000, "net_profit_cr": 55000, "opm_pct": 15.5},
        {"symbol": "RELIANCE", "company_name": "Reliance Industries", "sector": "Energy", "face_value": 10, "book_value": 800, "revenue_cr": 800000, "net_profit_cr": 68000, "opm_pct": 12.5},
        {"symbol": "TATAMOTORS", "company_name": "Tata Motors", "sector": "Auto", "face_value": 2, "book_value": 95, "revenue_cr": 350000, "net_profit_cr": 28000, "opm_pct": 8.5},
        {"symbol": "SUNPHARMA", "company_name": "Sun Pharma", "sector": "Pharma", "face_value": 1, "book_value": 110, "revenue_cr": 45000, "net_profit_cr": 9000, "opm_pct": 20.0},
        {"symbol": "HINDUNILVR", "company_name": "Hindustan Unilever", "sector": "FMCG", "face_value": 1, "book_value": 280, "revenue_cr": 60000, "net_profit_cr": 10000, "opm_pct": 19.5},
        {"symbol": "ITC", "company_name": "ITC Limited", "sector": "FMCG", "face_value": 1, "book_value": 85, "revenue_cr": 70000, "net_profit_cr": 20000, "opm_pct": 28.5},
        {"symbol": "BAJFINANCE", "company_name": "Bajaj Finance", "sector": "NBFC", "face_value": 2, "book_value": 350, "revenue_cr": 50000, "net_profit_cr": 12000, "opm_pct": 24.0},
        {"symbol": "ULTRACEMCO", "company_name": "UltraTech Cement", "sector": "Cement", "face_value": 10, "book_value": 220, "revenue_cr": 65000, "net_profit_cr": 8000, "opm_pct": 16.5},
        {"symbol": "BHARTIARTL", "company_name": "Bharti Airtel", "sector": "Telecom", "face_value": 5, "book_value": 95, "revenue_cr": 150000, "net_profit_cr": 12000, "opm_pct": 18.5},
    ]
    
    return JsonResponse({
        'success': True,
        'total': len(companies),
        'companies': companies
    })

@csrf_exempt
def company_detail(request, symbol):
    """Get detailed company information"""
    companies_data = {
        "TCS": {"name": "Tata Consultancy Services", "sector": "IT", "revenue_cr": 240000, "market_cap_cr": 1200000, "net_profit_cr": 45000, "opm_pct": 25.5, "ceo": "K Krithivasan", "employees": 600000, "face_value": 1, "book_value": 250},
        "INFY": {"name": "Infosys Limited", "sector": "IT", "revenue_cr": 150000, "market_cap_cr": 600000, "net_profit_cr": 28000, "opm_pct": 24.5, "ceo": "Salil Parekh", "employees": 300000, "face_value": 5, "book_value": 180},
        "HDFCBANK": {"name": "HDFC Bank", "sector": "Banking", "revenue_cr": 180000, "market_cap_cr": 900000, "net_profit_cr": 35000, "opm_pct": 20.5, "ceo": "Sashidhar Jagdishan", "employees": 150000, "face_value": 1, "book_value": 450},
        "RELIANCE": {"name": "Reliance Industries", "sector": "Energy", "revenue_cr": 800000, "market_cap_cr": 1500000, "net_profit_cr": 68000, "opm_pct": 12.5, "ceo": "Mukesh Ambani", "employees": 400000, "face_value": 10, "book_value": 800},
        "TATAMOTORS": {"name": "Tata Motors", "sector": "Auto", "revenue_cr": 350000, "market_cap_cr": 300000, "net_profit_cr": 28000, "opm_pct": 8.5, "ceo": "P Balaji", "employees": 80000, "face_value": 2, "book_value": 95},
        "SBIN": {"name": "State Bank of India", "sector": "Banking", "revenue_cr": 400000, "market_cap_cr": 550000, "net_profit_cr": 55000, "opm_pct": 15.5, "ceo": "Dinesh Kumar Khara", "employees": 250000, "face_value": 1, "book_value": 280},
    }
    
    symbol_upper = symbol.upper()
    if symbol_upper in companies_data:
        data = companies_data[symbol_upper]
        return JsonResponse({
            'symbol': symbol_upper,
            'company_name': data['name'],
            'sector': data['sector'],
            'revenue_cr': data['revenue_cr'],
            'market_cap_cr': data['market_cap_cr'],
            'net_profit_cr': data['net_profit_cr'],
            'opm_pct': data['opm_pct'],
            'ceo': data.get('ceo'),
            'employees': data.get('employees'),
        })
    else:
        return JsonResponse({'error': f'Company {symbol} not found'}, status=404)

@csrf_exempt
def company_financials(request, symbol):
    """Get historical financial data for a company"""
    historical_data = {
        "TCS": [
            {'year': 'Mar 2024', 'sales': 240000, 'net_profit': 45000, 'opm': 25.5, 'eps': 125.00},
            {'year': 'Mar 2023', 'sales': 215000, 'net_profit': 40000, 'opm': 24.8, 'eps': 112.00},
            {'year': 'Mar 2022', 'sales': 190000, 'net_profit': 35000, 'opm': 23.9, 'eps': 98.00},
        ],
        "INFY": [
            {'year': 'Mar 2024', 'sales': 150000, 'net_profit': 28000, 'opm': 24.5, 'eps': 85.00},
            {'year': 'Mar 2023', 'sales': 135000, 'net_profit': 25000, 'opm': 23.8, 'eps': 76.00},
            {'year': 'Mar 2022', 'sales': 120000, 'net_profit': 22000, 'opm': 22.5, 'eps': 68.00},
        ],
        "HDFCBANK": [
            {'year': 'Mar 2024', 'sales': 180000, 'net_profit': 35000, 'opm': 20.5, 'eps': 95.00},
            {'year': 'Mar 2023', 'sales': 160000, 'net_profit': 31000, 'opm': 19.8, 'eps': 85.00},
            {'year': 'Mar 2022', 'sales': 140000, 'net_profit': 27000, 'opm': 18.5, 'eps': 74.00},
        ],
        "RELIANCE": [
            {'year': 'Mar 2024', 'sales': 800000, 'net_profit': 68000, 'opm': 12.5, 'eps': 102.00},
            {'year': 'Mar 2023', 'sales': 750000, 'net_profit': 62000, 'opm': 11.8, 'eps': 93.00},
            {'year': 'Mar 2022', 'sales': 700000, 'net_profit': 58000, 'opm': 11.0, 'eps': 87.00},
        ],
    }
    
    symbol_upper = symbol.upper()
    if symbol_upper in historical_data:
        return JsonResponse({
            'symbol': symbol_upper,
            'historical_data': historical_data[symbol_upper]
        })
    else:
        return JsonResponse({'error': 'Financial data not found'}, status=404)

@csrf_exempt
def top_performers(request):
    """Get top performing companies - Top 10"""
    return JsonResponse({
        'metric': 'net_profit_growth',
        'year': 'Mar 2024',
        'top_performers': [
            {'rank': 1, 'symbol': 'TCS', 'company_name': 'Tata Consultancy Services', 'net_profit_growth': 18.5, 'net_profit_cr': 45000},
            {'rank': 2, 'symbol': 'HDFCBANK', 'company_name': 'HDFC Bank', 'net_profit_growth': 16.2, 'net_profit_cr': 35000},
            {'rank': 3, 'symbol': 'RELIANCE', 'company_name': 'Reliance Industries', 'net_profit_growth': 15.8, 'net_profit_cr': 68000},
            {'rank': 4, 'symbol': 'INFY', 'company_name': 'Infosys Limited', 'net_profit_growth': 14.5, 'net_profit_cr': 28000},
            {'rank': 5, 'symbol': 'SBIN', 'company_name': 'State Bank of India', 'net_profit_growth': 12.5, 'net_profit_cr': 55000},
            {'rank': 6, 'symbol': 'ICICIBANK', 'company_name': 'ICICI Bank', 'net_profit_growth': 11.8, 'net_profit_cr': 32000},
            {'rank': 7, 'symbol': 'HCLTECH', 'company_name': 'HCL Technologies', 'net_profit_growth': 10.5, 'net_profit_cr': 22000},
            {'rank': 8, 'symbol': 'BAJFINANCE', 'company_name': 'Bajaj Finance', 'net_profit_growth': 9.8, 'net_profit_cr': 12000},
            {'rank': 9, 'symbol': 'TATAMOTORS', 'company_name': 'Tata Motors', 'net_profit_growth': 8.5, 'net_profit_cr': 28000},
            {'rank': 10, 'symbol': 'WIPRO', 'company_name': 'Wipro Limited', 'net_profit_growth': 7.2, 'net_profit_cr': 15000},
            {'rank': 11, 'symbol': 'KOTAKBANK', 'company_name': 'Kotak Mahindra Bank', 'net_profit_growth': 6.5, 'net_profit_cr': 18000},
            {'rank': 12, 'symbol': 'SUNPHARMA', 'company_name': 'Sun Pharma', 'net_profit_growth': 5.8, 'net_profit_cr': 9000},
            {'rank': 13, 'symbol': 'HINDUNILVR', 'company_name': 'Hindustan Unilever', 'net_profit_growth': 5.2, 'net_profit_cr': 10000},
            {'rank': 14, 'symbol': 'ITC', 'company_name': 'ITC Limited', 'net_profit_growth': 4.8, 'net_profit_cr': 20000},
            {'rank': 15, 'symbol': 'ULTRACEMCO', 'company_name': 'UltraTech Cement', 'net_profit_growth': 4.2, 'net_profit_cr': 8000},
        ]
    })

@csrf_exempt
def sector_analysis(request):
    """Get sector-wise analysis"""
    return JsonResponse({
        'year': 'Mar 2024',
        'sectors': [
            {'sector': 'IT', 'total_sales_cr': 600000, 'total_profit_cr': 110000, 'avg_opm_pct': 23.8, 'companies': 4},
            {'sector': 'Banking', 'total_sales_cr': 730000, 'total_profit_cr': 122000, 'avg_opm_pct': 18.2, 'companies': 3},
            {'sector': 'Energy', 'total_sales_cr': 800000, 'total_profit_cr': 68000, 'avg_opm_pct': 12.3, 'companies': 1},
            {'sector': 'Auto', 'total_sales_cr': 350000, 'total_profit_cr': 28000, 'avg_opm_pct': 8.5, 'companies': 1},
            {'sector': 'FMCG', 'total_sales_cr': 130000, 'total_profit_cr': 30000, 'avg_opm_pct': 24.0, 'companies': 2},
        ]
    })

# ============================================================
# FRONTEND PAGE VIEWS
# ============================================================

def dashboard(request):
    """Render dashboard page"""
    return render(request, 'dashboard.html')

def companies_list_page(request):
    """Render companies list page"""
    return render(request, 'companies.html')

def company_detail_page(request, symbol):
    """Render company detail page"""
    return render(request, 'company_detail.html', {'symbol': symbol})

def top_performers_page(request):
    """Render top performers page"""
    return render(request, 'top_performers.html')

def sector_analysis_page(request):
    """Render sector analysis page"""
    return render(request, 'sector_analysis.html')