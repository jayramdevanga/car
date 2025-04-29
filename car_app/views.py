from django.shortcuts import render
import json
import os

# Load JSON only once to avoid reading on every request
json_path = os.path.join(os.path.dirname(__file__), '..', 'templete', 'car_data.json')
with open(json_path, 'r') as file:
    py_data = json.load(file)

cars = py_data

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def car_rent(request):
    return render(request, 'car_rent.html', {'cars': cars})

def car_detail(request, car_id):
    car = next((c for c in cars if str(c["id"]) == str(car_id)), None)
    if car is None:
        return render(request, '404.html', status=404)
    return render(request, 'car_detail.html', {'car': car})

