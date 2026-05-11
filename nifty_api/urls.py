<<<<<<< HEAD
from django.urls import path
=======
﻿from django.urls import path
>>>>>>> 28b90ff430cf4491e0405520df52cbc251e2c053
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('health/', views.health_check, name='health'),
    path('companies/', views.company_list, name='company-list'),
    path('companies/<str:symbol>/', views.company_detail, name='company-detail'),
    path('top-performers/', views.top_performers, name='top-performers'),
    path('sector-analysis/', views.sector_analysis, name='sector-analysis'),
]
