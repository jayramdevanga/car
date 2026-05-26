from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking
from datetime import datetime

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def car_rent(request):
    cars = Car.objects.all()
    return render(request, 'car_rent.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            days = (end_date - start_date).days
            
            if days > 0:
                total_price = float(days * car.price_per_day)
                
                # Save data into session to use on the payment page
                request.session['booking_data'] = {
                    'car_id': car.id,
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                    'total_price': total_price
                }
                # Redirect straight to the payment route
                return redirect('payment')

    return render(request, 'car_detail.html', {'car': car})

def payment(request):
    # Grab the booking details from the session
    booking_data = request.session.get('booking_data')
    
    if not booking_data:
        return redirect('car_rent')
        
    car = get_object_or_404(Car, id=booking_data['car_id'])
    
    if request.method == 'POST':
        # If they click "Pay Now", finalize and save to database
        if request.user.is_authenticated:
            start_date = datetime.strptime(booking_data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(booking_data['end_date'], '%Y-%m-%d').date()
            
            booking = Booking.objects.create(
                user=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
                total_price=booking_data['total_price']
            )
            
            # Clear session now that it's saved
            del request.session['booking_data']
            
            return render(request, 'payment.html', {'success': True, 'car': car})
            
        else:
            return redirect('admin:index') # Fallback login path

    return render(request, 'payment.html', {
        'car': car,
        'booking_data': booking_data
    })
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_gateway(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # If they are staff/admin, send them to the Django admin panel
                if user.is_staff:
                    return redirect('admin:index')
                # Otherwise, send regular users to the car fleet catalog
                return redirect('car_rent')
            else:
                error_message = "Invalid username or password."
        else:
            error_message = "Invalid username or password."
            
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('home')
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register_gateway(request):
    if request.user.is_authenticated:
        return redirect('car_rent')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car_rent')
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Car

@login_required
def booking_pending_view(request, booking_id):
    # Safely fetch the booking belonging to the logged-in user
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_pending.html', {'booking': booking})