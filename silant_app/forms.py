from django import forms
from django.views.generic import CreateView

from .models.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class TechnicalMaintenanceCreateForm(forms.ModelForm):
    machine_serial_number = forms.ModelChoiceField(queryset=Machine.objects.all(), label='Serial Number')
    service_company = forms.ModelChoiceField(queryset=ServiceCompanyReference.objects.all(), label="Service Company")
    maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    order_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TechnicalMaintenance
        fields = ['machine_serial_number', 'maintenance_type', 'maintenance_date', 'order_number', 'order_date', 'service_company']

    def clean(self):
        cleaned_data = super().clean()
        machine = cleaned_data.get('machine_serial_number')
        service_company = cleaned_data.get('service_company')

        if machine and service_company and machine.service_company != service_company:
            self.add_error('service_company', 'The service company must match the one assigned to the machine.')
        return cleaned_data


class TechnicalMaintenanceUpdateForm(forms.ModelForm):
    service_company = forms.ModelChoiceField(queryset=ServiceCompanyReference.objects.all(), label="Service Company")
    maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    order_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TechnicalMaintenance
        fields = ['maintenance_type', 'maintenance_date', 'order_number', 'order_date', 'service_company']

    def clean(self):
        cleaned_data = super().clean()
        service_company = cleaned_data.get('service_company')
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_service_company')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_service_company')



class ClaimCreateForm(forms.ModelForm):
    machine_serial_number = forms.ModelChoiceField(queryset=Machine.objects.all(), label='Serial Number')
    service_company = forms.ModelChoiceField(queryset=ServiceCompanyReference.objects.all(), label="Service Company")
    failure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    recovery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Claim
        fields = ['machine_serial_number', 'failure_date', 'operating_hours', 'failure_unit', 'failure_description', 'recovery_method', 'used_spare_parts', 'recovery_date', 'service_company']

    def clean(self):
        cleaned_data = super().clean()
        machine = cleaned_data.get('machine_serial_number')
        service_company = cleaned_data.get('service_company')
        failure_date = cleaned_data.get('failure_date')
        recovery_date = cleaned_data.get('recovery_date')

        if machine and service_company and machine.service_company != service_company:
            self.add_error('service_company', 'The service company must match the one assigned to the machine.')

        if recovery_date and failure_date and recovery_date <= failure_date:
            self.add_error('recovery_date', 'Recovery date must be after the failure date.')

        return cleaned_data

class ClaimUpdateForm(forms.ModelForm):
    service_company = forms.ModelChoiceField(queryset=ServiceCompanyReference.objects.all(), label="Service Company")
    failure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    recovery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Claim
        fields = ['failure_date', 'operating_hours', 'failure_unit', 'failure_description', 'recovery_method', 'used_spare_parts', 'recovery_date', 'service_company']

    def clean(self):
        cleaned_data = super().clean()
        service_company = cleaned_data.get('service_company')
        failure_date = cleaned_data.get('failure_date')
        recovery_date = cleaned_data.get('recovery_date')

        if recovery_date and failure_date and recovery_date <= failure_date:
            self.add_error('recovery_date', 'Recovery date must be after the failure date.')

        return cleaned_data
