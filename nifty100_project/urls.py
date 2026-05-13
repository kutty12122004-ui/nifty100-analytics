from django.contrib import admin
from django.urls import path, include
from nifty_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nifty_api.urls')),  # This should include all URLs from nifty_api
]