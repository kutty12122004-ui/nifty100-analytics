# nifty_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('', views.api_root, name='api-root'),
    path('health/', views.health_check, name='health'),
    path('companies/', views.company_list, name='company-list'),
    path('companies/<str:symbol>/', views.company_detail, name='company-detail'),
    path('companies/<str:symbol>/financials/', views.company_financials, name='company-financials'),
    path('top-performers/', views.top_performers, name='top-performers'),
    path('sector-analysis/', views.sector_analysis, name='sector-analysis'),
]