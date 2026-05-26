from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),            # <-- Added the missing 's' right here!
    path('', include('car_app.urls')), 
    path('accounts/', include('allauth.urls')), 
]