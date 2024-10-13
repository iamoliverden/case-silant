from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django_filters.views import *
from .filters import *


def landing_page(request):
    return render(request, 'landing_page.html')


def search(request):
    serial_number = request.GET.get('serial_number')
    if serial_number:
        search_results = Machine.objects.filter(serial_number=serial_number).order_by('shipment_date')
    else:
        search_results = None
    return render(request, 'landing_page.html', {'search_results': search_results})


def detailed_info_unauth(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    user_name = request.user.username
    return render(request, 'detailed_info_unauth.html', {'machine': machine, 'user_name': user_name})


@login_required
def detailed_info_auth(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    user_name = request.user.username
    return render(request, 'detailed_info_auth.html', {'machine': machine, 'user_name': user_name})


@login_required
def technical_maintenance(request):
    serial_number = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=serial_number).first()
    maintenances = TechnicalMaintenance.objects.filter(machine=machine).order_by(
        'maintenance_date') if machine else None
    user_name = request.user.username

    # Check if the user belongs to groups 1, 3, or 5
    user_groups = request.user.groups.values_list('id', flat=True)
    can_edit_or_add = any(group_id in [1, 3, 5] for group_id in user_groups)

    return render(request, 'technical_maintenance.html', {
        'machine': machine,
        'maintenances_records': maintenances,
        'user_name': user_name,
        'can_edit_or_add': can_edit_or_add
    })


class ClaimPermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1, 3, 4, 5] for group_id in user_groups)


class MachinePermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('id', flat=True)
        return any(group_id in [1] for group_id in user_groups)


class ClaimListView(LoginRequiredMixin, ClaimPermissions, ListView):
    model = Claim
    template_name = 'claims.html'
    context_object_name = 'claims'
    filterset_class = ClaimFilter

    def get_queryset(self):
        serial_number = self.request.GET.get('serial_number')
        machine = Machine.objects.filter(serial_number=serial_number).first()
        if machine:
            return Claim.objects.filter(machine=machine).order_by('failure_date')
        else:
            return Claim.objects.none()

    def can_edit_or_add(self):
        # Check if the user belongs to groups 1, 3, or 5
        user_groups = self.request.user.groups.values_list('id', flat=True)
        can_edit_or_add = any(group_id in [1, 3, 5] for group_id in user_groups)
        return can_edit_or_add

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filterset(self.filterset_class)
        context['user_name'] = self.request.user.username
        context['can_edit_or_add'] = self.can_edit_or_add()
        return context

    def get_filterset(self, filterset_class):
        return filterset_class(self.request.GET, queryset=self.get_queryset())


class ClaimDetailView(LoginRequiredMixin, ClaimPermissions, DetailView):
    model = Claim
    template_name = 'claims_detailed.html'
    context_object_name = 'claim'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user.username
        return context


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page_logged_in')  # Use the correct URL name here
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('landing_page')


@login_required
def landing_page_logged_in(request):
    user_machines = Machine.objects.filter(client=request.user).order_by('shipment_date')
    user_name = request.user.username
    user_groups = request.user.groups.values_list('id', flat=True)
    is_manager = request.user.groups.filter(id=1).exists()
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


@login_required
def search_ent(request):
    serial_number = request.GET.get('serial_number')
    user_name = request.user.username
    if serial_number:
        search_results = Machine.objects.filter(serial_number=serial_number).order_by('shipment_date')
    else:
        search_results = None
    return render(request, 'landing_page_ent.html', {
        'search_results': search_results,
        'user_name': user_name
    })


class MaintenanceRecordPermissions(UserPassesTestMixin):
    def test_func(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return any(group in ['Service Companies', 'Managers', 'Admins'] for group in user_groups)


class TechnicalMaintenanceCreateView(LoginRequiredMixin, MaintenanceRecordPermissions, CreateView):
    model = TechnicalMaintenance
    form_class = TechnicalMaintenanceCreateForm
    template_name = 'create_service_record.html'

    def form_valid(self, form):
        order_date = form.cleaned_data['order_date']
        maintenance_date = form.cleaned_data['maintenance_date']

        if maintenance_date <= order_date:
            form.add_error('maintenance_date', 'Maintenance date must be after the order date.')
            return self.form_invalid(form)

        form.instance.machine = form.cleaned_data['machine_serial_number']
        form.instance.operating_hours = (maintenance_date - order_date).days * 24

        if TechnicalMaintenance.objects.filter(order_number=form.cleaned_data['order_number'],
                                               service_company=form.cleaned_data['service_company']).exists():
            form.add_error('order_number', 'Order number must be unique for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('technical_maintenance') + f'?serial_number={self.object.machine.serial_number}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class TechnicalMaintenanceUpdateView(LoginRequiredMixin, MaintenanceRecordPermissions, UpdateView):
    model = TechnicalMaintenance
    form_class = TechnicalMaintenanceUpdateForm
    template_name = 'edit_service_record.html'

    def form_valid(self, form):
        order_date = form.cleaned_data['order_date']
        maintenance_date = form.cleaned_data['maintenance_date']

        if maintenance_date <= order_date:
            form.add_error('maintenance_date', 'Maintenance date must be after the order date.')
            return self.form_invalid(form)

        form.instance.operating_hours = (maintenance_date - order_date).days * 24

        if TechnicalMaintenance.objects.filter(
                order_number=form.cleaned_data['order_number'],
                service_company=form.cleaned_data['service_company']
        ).exclude(pk=self.object.pk).exists():
            form.add_error('order_number', 'Order number must be unique for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('technical_maintenance') + f'?serial_number={self.object.machine.serial_number}'


class ClaimCreateView(CreateView):
    model = Claim
    form_class = ClaimCreateForm
    template_name = 'create_claim.html'

    def form_valid(self, form):
        failure_date = form.cleaned_data['failure_date']
        recovery_date = form.cleaned_data['recovery_date']

        if recovery_date <= failure_date:
            form.add_error('recovery_date', 'Recovery date must be after the failure date.')
            return self.form_invalid(form)

        form.instance.machine = form.cleaned_data['machine_serial_number']
        form.instance.downtime = (recovery_date - failure_date).days

        if Claim.objects.filter(failure_date=failure_date,
                                service_company=form.cleaned_data['service_company']).exists():
            form.add_error('failure_date', 'A claim with this failure date already exists for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('claims') + f'?serial_number={self.object.machine.serial_number}'


class ClaimUpdateView(UpdateView):
    model = Claim
    form_class = ClaimUpdateForm
    template_name = 'edit_claim.html'

    def form_valid(self, form):
        failure_date = form.cleaned_data['failure_date']
        recovery_date = form.cleaned_data['recovery_date']

        if recovery_date <= failure_date:
            form.add_error('recovery_date', 'Recovery date must be after the failure date.')
            return self.form_invalid(form)

        form.instance.downtime = (recovery_date - failure_date).days

        if Claim.objects.filter(
                failure_date=failure_date,
                service_company=form.cleaned_data['service_company']
        ).exclude(pk=self.object.pk).exists():
            form.add_error('failure_date', 'A claim with this failure date already exists for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('claims') + f'?serial_number={self.object.machine.serial_number}'


class MachineCreateView(MachinePermissions, CreateView):
    model = Machine
    form_class = MachineCreateForm
    template_name = 'create_machine.html'

    def form_valid(self, form):
        # Add any additional validation or processing here if needed
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detailed_info_auth') + f'?serial_number={self.object.serial_number}'

    def is_manager(self):
        # Check if the user belongs to groups 1, 3, or 5
        user_groups = self.request.user.groups.values_list('id', flat=True)
        is_manager = any(group_id in [1] for group_id in user_groups)
        return is_manager


class MachineUpdateView(MachinePermissions, UpdateView):
    model = Machine
    form_class = MachineUpdateForm
    template_name = 'edit_machine.html'

    def get_queryset(self):
        serial_number = self.request.GET.get('serial_number')
        machine = Machine.objects.filter(serial_number=serial_number).first()
        return machine

    def form_valid(self, form):
        # Add any additional validation or processing here if needed
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detailed_info_auth') + f'?serial_number={self.object.serial_number}'

    def is_manager(self):
        # Check if the user belongs to groups 1, 3, or 5
        user_groups = self.request.user.groups.values_list('id', flat=True)
        is_manager = any(group_id in [1] for group_id in user_groups)
        return is_manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_queryset()
        context['is_manager'] = self.is_manager()
        return context
