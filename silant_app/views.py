from .models import Machine, TechnicalMaintenance, Claim
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def landing_page(request):
    return render(request, 'landing_page.html')

def search(request):
    serial_number = request.GET.get('serial_number')
    search_results = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'landing_page.html', {'search_results': search_results})

@login_required
def landing_page_loggedin(request):
    return render(request, 'landing_page_loggedin.html')

@login_required
def search_loggedin(request):
    serial_number = request.GET.get('serial_number')
    search_results = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'landing_page_loggedin.html', {'search_results': search_results})

@login_required
def general_info(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    return render(request, 'general_info.html', {'machine': machine})

@login_required
def technical_maintenance(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    maintenances = TechnicalMaintenance.objects.filter(machine=machine) if machine else None
    return render(request, 'technical_maintenance.html', {'maintenances': maintenances})

@login_required
def claims(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    claims = Claim.objects.filter(machine=machine) if machine else None
    return render(request, 'claims.html', {'claims': claims})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page_loggedin')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')