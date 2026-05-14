from django.urls import path
from nifty_api import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('companies/', views.companies_list_page, name='companies'),
    path('company/<str:symbol>/', views.company_detail_page, name='company_detail'),
    path('top-performers/', views.top_performers_page, name='top_performers'),
    path('sector-analysis/', views.sector_analysis_page, name='sector_analysis'),
    path('api/', views.api_root, name='api_root'),
    path('api/health/', views.health_check, name='health_check'),
    path('api/companies/', views.company_list, name='company_list'),
    path('api/companies/<str:symbol>/', views.company_detail, name='company_detail'),
    path('api/top-performers/', views.top_performers, name='top_performers'),
    path('api/sector-analysis/', views.sector_analysis, name='sector_analysis'),
]
