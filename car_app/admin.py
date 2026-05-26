from django.contrib import admin
from .models import Car, Booking

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # This controls what details you see in the admin list view
    list_display = ('make', 'model', 'year', 'car_type', 'price_per_day', 'available')
    list_filter = ('available', 'car_type', 'location')
    search_fields = ('make', 'model', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price')
    list_filter = ('start_date', 'end_date')