from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView


def landing_page(request):
    return render(request, 'landing_page.html')


def search(request):
    serial_number = request.GET.get('serial_number')
    search_results = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'landing_page.html', {'search_results': search_results})


@login_required
def detailed_info(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    user_name = request.user.username
    return render(request, 'detailed_info.html', {'machine': machine, 'user_name': user_name})

@login_required
def technical_maintenance(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    maintenances = TechnicalMaintenance.objects.filter(machine=machine) if machine else None
    user_name = request.user.username
    return render(request, 'technical_maintenance.html', {
        'machine': machine,
        'maintenances_records': maintenances,
        'user_name': user_name
    })


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
            return redirect('landing_page_logged_in')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('landing_page')


@login_required
def landing_page_logged_in(request):
    user_machines = Machine.objects.filter(client=request.user)
    user_name = request.user.username
    return render(request, 'landing_page_logged_in.html', {
        'user_machines': user_machines,
        'user_name': user_name
    })


class ServiceCompanyRequiredMixin(UserPassesTestMixin):
    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.groups.filter(name='Service Company').exists()


class TechnicalMaintenanceCreateView(LoginRequiredMixin, ServiceCompanyRequiredMixin, CreateView):
    model = TechnicalMaintenance
    form_class = TechnicalMaintenanceForm
    template_name = 'create_service_record.html'

    def form_valid(self, form):
        form.instance.machine = form.cleaned_data['machine_serial_number']
        form.instance.operating_hours = (form.cleaned_data['maintenance_date'] - form.cleaned_data['order_date']).days
        if TechnicalMaintenance.objects.filter(order_number=form.cleaned_data['order_number'],
                                               service_company=form.cleaned_data['service_company']).exists():
            form.add_error('order_number', 'Order number must be unique for this service company.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('technical_maintenance') + f'?machine_id={self.object.machine.id}'


class TechnicalMaintenanceUpdateView(LoginRequiredMixin, ServiceCompanyRequiredMixin, UpdateView):
    model = TechnicalMaintenance
    form_class = TechnicalMaintenanceForm
    template_name = 'edit_service_record.html'

    def form_valid(self, form):
        form.instance.machine = form.cleaned_data['machine_serial_number']
        form.instance.operating_hours = (form.cleaned_data['maintenance_date'] - form.cleaned_data['order_date']).days
        if TechnicalMaintenance.objects.filter(order_number=form.cleaned_data['order_number'],
                                               service_company=form.cleaned_data['service_company']).exclude(
                pk=self.object.pk).exists():
            form.add_error('order_number', 'Order number must be unique for this service company.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('technical_maintenance') + f'?machine_id={self.object.machine.id}'
