# create_views.py

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from silant_app.forms import TechnicalMaintenanceCreateForm, ClaimCreateForm, MachineCreateForm
from silant_app.models import TechnicalMaintenance, Claim, Machine
from silant_app.views.views_permissions import MaintenanceRecordPermissions, MachinePermissions

from django.contrib.auth.mixins import LoginRequiredMixin


# Technical Maintenance Create View
class TechnicalMaintenanceCreateView(LoginRequiredMixin, MaintenanceRecordPermissions, CreateView):
    model = TechnicalMaintenance
    form_class = TechnicalMaintenanceCreateForm
    template_name = 'create_service_record.html'

    def form_valid(self, form):
        # Validate dates and ensure maintenance date is after order date
        order_date = form.cleaned_data['order_date']
        maintenance_date = form.cleaned_data['maintenance_date']

        if maintenance_date <= order_date:
            form.add_error('maintenance_date', 'Maintenance date must be after the order date.')
            return self.form_invalid(form)

        # Assign machine and calculate operating hours
        form.instance.machine = form.cleaned_data['machine_serial_number']
        form.instance.operating_hours = (maintenance_date - order_date).days * 24

        # Ensure the order number is unique for the service company
        if TechnicalMaintenance.objects.filter(order_number=form.cleaned_data['order_number'],
                                               service_company=form.cleaned_data['service_company']).exists():
            form.add_error('order_number', 'Order number must be unique for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the technical maintenance list with the machine's serial number
        return reverse_lazy('technical_maintenance') + f'?serial_number={self.object.machine.serial_number}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


# Claim Create View
class ClaimCreateView(CreateView):
    model = Claim
    form_class = ClaimCreateForm
    template_name = 'create_claim.html'

    def form_valid(self, form):
        # Validate that recovery date is after failure date
        failure_date = form.cleaned_data['failure_date']
        recovery_date = form.cleaned_data['recovery_date']

        if recovery_date <= failure_date:
            form.add_error('recovery_date', 'Recovery date must be after the failure date.')
            return self.form_invalid(form)

        # Assign machine and calculate downtime
        form.instance.machine = form.cleaned_data['machine_serial_number']
        form.instance.downtime = (recovery_date - failure_date).days

        # Ensure claim for failure date and service company is unique
        if Claim.objects.filter(failure_date=failure_date,
                                service_company=form.cleaned_data['service_company']).exists():
            form.add_error('failure_date', 'A claim with this failure date already exists for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to claims list with the machine's serial number
        return reverse_lazy('claims') + f'?serial_number={self.object.machine.serial_number}'


# Machine Create View
class MachineCreateView(MachinePermissions, CreateView):
    model = Machine
    form_class = MachineCreateForm
    template_name = 'create_machine.html'

    def form_valid(self, form):
        # Add any additional validation or processing here if needed
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to detailed information view with the machine's serial number
        return reverse_lazy('detailed_info_auth') + f'?serial_number={self.object.serial_number}'

    def is_manager(self):
        # Check if the user belongs to the 'manager' group (group 1)
        user_groups = self.request.user.groups.values_list('id', flat=True)
        is_manager = any(group_id in [1] for group_id in user_groups)
        return is_manager
