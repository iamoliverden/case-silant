# update_views.py

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from silant_app.forms import TechnicalMaintenanceUpdateForm, ClaimUpdateForm, MachineUpdateForm
from silant_app.models import TechnicalMaintenance, Claim, Machine
from silant_app.views.views_permissions import MaintenanceRecordPermissions, MachinePermissions, ClaimPermissions

from django.contrib.auth.mixins import LoginRequiredMixin


# Technical Maintenance Update View
class TechnicalMaintenanceUpdateView(LoginRequiredMixin, MaintenanceRecordPermissions, UpdateView):
    model = TechnicalMaintenance
    form_class = TechnicalMaintenanceUpdateForm
    template_name = 'edit_service_record.html'

    def form_valid(self, form):
        # Validate that maintenance date is after order date
        order_date = form.cleaned_data['order_date']
        maintenance_date = form.cleaned_data['maintenance_date']

        if maintenance_date <= order_date:
            form.add_error('maintenance_date', 'Maintenance date must be after the order date.')
            return self.form_invalid(form)

        # Calculate and update operating hours
        form.instance.operating_hours = (maintenance_date - order_date).days * 24

        # Ensure unique order number per service company, excluding current instance
        if TechnicalMaintenance.objects.filter(
                order_number=form.cleaned_data['order_number'],
                service_company=form.cleaned_data['service_company']
        ).exclude(pk=self.object.pk).exists():
            form.add_error('order_number', 'Order number must be unique for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to technical maintenance list with machine serial number
        return reverse_lazy('technical_maintenance') + f'?serial_number={self.object.machine.serial_number}'


# Claim Update View
class ClaimUpdateView(LoginRequiredMixin, ClaimPermissions, UpdateView):
    model = Claim
    form_class = ClaimUpdateForm
    template_name = 'edit_claim.html'

    def form_valid(self, form):
        # Validate that recovery date is after failure date
        failure_date = form.cleaned_data['failure_date']
        recovery_date = form.cleaned_data['recovery_date']

        if recovery_date <= failure_date:
            form.add_error('recovery_date', 'Recovery date must be after the failure date.')
            return self.form_invalid(form)

        # Calculate and update downtime
        form.instance.downtime = (recovery_date - failure_date).days

        # Ensure unique failure date for the service company, excluding current instance
        if Claim.objects.filter(
                failure_date=failure_date,
                service_company=form.cleaned_data['service_company']
        ).exclude(pk=self.object.pk).exists():
            form.add_error('failure_date', 'A claim with this failure date already exists for this service company.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to claims list with machine serial number
        return reverse_lazy('claims') + f'?serial_number={self.object.machine.serial_number}'



# Machine Update View
class MachineUpdateView(UpdateView):
    model = Machine
    form_class = MachineUpdateForm
    template_name = 'edit_machine.html'

    def get_object(self, queryset=None):
        # Get the machine object based on the primary key from the URL
        return super().get_object(queryset)

    def form_valid(self, form):
        # Additional validation or processing can be added here if needed
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to detailed information view with the machine serial number
        return reverse_lazy('detailed_info_auth') + f'?serial_number={self.object.serial_number}'

    def is_manager(self):
        # Check if the user belongs to the 'manager' group (group 1)
        user_groups = self.request.user.groups.values_list('id', flat=True)
        is_manager = any(group_id in [1, 5] for group_id in user_groups)
        return is_manager

    def get_context_data(self, **kwargs):
        # Add context data for machine details and manager status
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object()  # Add the machine instance to the context
        context['is_manager'] = self.is_manager()
        return context
