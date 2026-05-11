from django.urls import path
from . import views

urlpatterns = [
    # Frontend pages
    path('', views.dashboard, name='dashboard'),
    path('companies/', views.companies_list_page, name='companies'),
    path('company/<str:symbol>/', views.company_detail_page, name='company_detail'),
    path('top-performers/', views.top_performers_page, name='top_performers'),
    path('sector-analysis/', views.sector_analysis_page, name='sector_analysis'),
    
    # API endpoints
    path('api/', views.api_root, name='api_root'),
    path('api/companies/', views.api_company_list, name='api_company_list'),
    path('api/companies/all/', views.api_companies_full, name='api_companies_full'),
    path('api/sector-analysis/', views.api_sector_analysis, name='api_sector_analysis'),
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/company/<str:symbol>/', views.api_company_detail, name='api_company_detail'),
    path('api/health/', views.api_health, name='api_health'),
]