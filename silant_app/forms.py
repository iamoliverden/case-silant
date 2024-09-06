from django import forms
from .models.models import *


class TechnicalMaintenanceForm(forms.ModelForm):
    machine_serial_number = forms.ModelChoiceField(queryset=Machine.objects.all(), label="Machine Serial Number")
    service_company = forms.ModelChoiceField(queryset=ServiceCompanyReference.objects.all(), label="Service Company")
    maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    order_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TechnicalMaintenance
        fields = ['machine_serial_number', 'maintenance_type', 'maintenance_date', 'order_number', 'order_date',
                  'service_company']

    def clean(self):
        cleaned_data = super().clean()
        machine = cleaned_data.get('machine_serial_number')
        service_company = cleaned_data.get('service_company')

        if machine and service_company and machine.service_company != service_company:
            self.add_error('service_company', 'The service company must match the one assigned to the machine.')

        return cleaned_data
