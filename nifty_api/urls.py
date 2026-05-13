from django.urls import path
from . import views

urlpatterns = [
    # Web pages
    path('', views.dashboard, name='dashboard'),
    path('companies/', views.companies_list_page, name='companies'),
    path('company/<str:symbol>/', views.company_detail_page, name='company_detail'),
    path('top-performers/', views.top_performers_page, name='top_performers'),
    path('sector-analysis/', views.sector_analysis_page, name='sector_analysis'),
    
    # API endpoints
    path('api/', views.api_root, name='api_root'),
    path('api/companies/', views.company_list, name='api_company_list'),
    path('api/health/', views.health_check, name='health_check'),
]