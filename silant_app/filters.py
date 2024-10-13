# filters.py

import django_filters
from .models import *
from django import forms

class MachineFilter(django_filters.FilterSet):
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(field_name='model__name', lookup_expr='icontains')
    shipment_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Machine
        fields = ['serial_number', 'model', 'shipment_date']

class ClaimFilter(django_filters.FilterSet):
    machine_serial_number = django_filters.CharFilter(field_name='machine__serial_number', lookup_expr='icontains', label='Machine Serial Number')
    failure_date = django_filters.DateFilter(
        field_name='failure_date',
        lookup_expr='exact',
        label='Failure Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    service_company = django_filters.ModelChoiceFilter(queryset=ServiceCompanyReference.objects.all(), label='Service Company')

    class Meta:
        model = Claim
        fields = ['machine_serial_number', 'failure_date', 'service_company']
