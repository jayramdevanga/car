from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('carrent/', views.car_rent, name='car_rent'),
    path('carrent/<int:car_id>/', views.car_detail, name='car_detail'),
]
