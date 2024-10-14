# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from silant_app.models import Machine


# Landing page view (unauthenticated)
def landing_page(request):
    return render(request, 'landing_page.html')


# Search view for machine by serial number
def search(request):
    serial_number = request.GET.get('serial_number')
    search_results = Machine.objects.filter(serial_number=serial_number).order_by('shipment_date') if serial_number else None
    return render(request, 'landing_page.html', {'search_results': search_results})


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page_logged_in')  # Redirect after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('landing_page')


# Authenticated landing page
@login_required
def landing_page_logged_in(request):
    user_machines = Machine.objects.filter(client=request.user).order_by('shipment_date')
    user_name = request.user.username
    user_groups = request.user.groups.values_list('id', flat=True)
    is_manager = request.user.groups.filter(id=1).exists()

    # Determine which template to use based on user groups
    if any(group_id in [2, 4] for group_id in user_groups):
        return render(request, 'landing_page_auth.html', {
            'user_machines': user_machines,
            'user_name': user_name,
        })
    elif any(group_id in [1, 3, 5] for group_id in user_groups):
        return render(request, 'landing_page_ent.html', {
            'user_machines': user_machines,
            'user_name': user_name,
            'is_manager': is_manager
        })

