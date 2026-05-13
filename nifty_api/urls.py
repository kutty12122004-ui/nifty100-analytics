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
    path('api/companies/', views.company_list, name='api_company_list'),
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/sector-analysis/', views.api_sector_analysis, name='api_sector_analysis'),
    path('api/health/', views.api_health, name='api_health'),
]