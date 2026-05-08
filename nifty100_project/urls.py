# nifty100_project/urls.py
from django.contrib import admin
from django.urls import path, include
from nifty_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('nifty_api.urls')),
    
    # Frontend URLs - Make sure these names match what's in base.html
    path('', views.dashboard, name='dashboard'),
    path('companies/', views.companies_list_page, name='companies'),
    path('company/<str:symbol>/', views.company_detail_page, name='company_detail'),
    path('top-performers/', views.top_performers_page, name='top_performers'),
    path('sector-analysis/', views.sector_analysis_page, name='sector_analysis'),  # <- This name matches
]