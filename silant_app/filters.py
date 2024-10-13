import django_filters
from .models import *
from django import forms


class ClaimFilter(django_filters.FilterSet):

    serial_number = django_filters.ModelChoiceFilter(
        field_name='machine__serial_number',
        label='Machine Serial Number',
        widget=forms.Select()
    )

    machine_model = django_filters.ModelChoiceFilter(
        queryset=MachineModelReference.objects.all(),
        field_name='machine__model',
        label='Machine Model',
        widget=forms.Select()
    )
    engine_model = django_filters.ModelChoiceFilter(
        queryset=EngineModelReference.objects.all(),
        field_name='machine__engine_model',
        label='Engine Model',
        widget=forms.Select()
    )
    transmission_model = django_filters.ModelChoiceFilter(
        queryset=TransmissionModelReference.objects.all(),
        field_name='machine__transmission_model',
        label='Transmission Model',
        widget=forms.Select()
    )
    steer_axel_model = django_filters.ModelChoiceFilter(
        queryset=SteerAxleModelReference.objects.all(),
        field_name='machine__steer_axle_model',
        label='Steer Axle Model',
        widget=forms.Select()
    )
    drive_axel_model = django_filters.ModelChoiceFilter(
        queryset=DriveAxleModelReference.objects.all(),
        field_name='machine__drive_axle_model',
        label='Drive Axle Model',
        widget=forms.Select()
    )
    failure_date = django_filters.DateFilter(
        field_name='failure_date',
        lookup_expr='exact',
        label='Failure Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    service_company = django_filters.ModelChoiceFilter(
        queryset=ServiceCompanyReference.objects.all(),
        label='Service Company',
        widget=forms.Select()
    )
    failure_unit = django_filters.ModelChoiceFilter(
        queryset=FailureUnitReference.objects.all(),
        label='Failure Unit',
        widget=forms.Select()
    )
    recovery_method = django_filters.ModelChoiceFilter(
        queryset=RecoveryMethodReference.objects.all(),
        label='Recovery Method',
        widget=forms.Select()
    )

    class Meta:
        model = Claim
        fields = [
            'serial_number',
            'machine_model', 'engine_model',
            'transmission_model', 'steer_axel_model',
            'drive_axel_model', 'failure_date',
            'service_company', 'failure_unit',
            'recovery_method'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_groups = user.groups.values_list('id', flat=True)
            if 4 in user_groups:
                self.filters['serial_number'].queryset = Machine.objects.filter(client=user)
            else:
                self.filters['serial_number'].queryset = Machine.objects.all()

class GeneralInformationFilter(django_filters.FilterSet):
    serial_number = django_filters.CharFilter(
        field_name='serial_number',
        lookup_expr='icontains',
        label='Machine Serial Number',
        widget=forms.TextInput()
    )
    machine_model = django_filters.ModelChoiceFilter(
        queryset=MachineModelReference.objects.all(),
        field_name='model',
        label='Machine Model',
        widget=forms.Select()
    )
    engine_model = django_filters.ModelChoiceFilter(
        queryset=EngineModelReference.objects.all(),
        field_name='engine_model',
        label='Engine Model',
        widget=forms.Select()
    )
    transmission_model = django_filters.ModelChoiceFilter(
        queryset=TransmissionModelReference.objects.all(),
        field_name='transmission_model',
        label='Transmission Model',
        widget=forms.Select()
    )
    steer_axel_model = django_filters.ModelChoiceFilter(
        queryset=SteerAxleModelReference.objects.all(),
        field_name='steer_axle_model',
        label='Steer Axle Model',
        widget=forms.Select()
    )
    drive_axel_model = django_filters.ModelChoiceFilter(
        queryset=DriveAxleModelReference.objects.all(),
        field_name='drive_axle_model',
        label='Drive Axle Model',
        widget=forms.Select()
    )
    service_company = django_filters.ModelChoiceFilter(
        queryset=ServiceCompanyReference.objects.all(),
        label='Service Company',
        widget=forms.Select()
    )

    class Meta:
        model = Machine
        fields = [
            'serial_number', 'machine_model', 'engine_model',
            'transmission_model', 'steer_axel_model',
            'drive_axel_model', 'service_company'
        ]



class TechnicalMaintenanceFilter(django_filters.FilterSet):
    serial_number = django_filters.ModelChoiceFilter(
        field_name='machine__serial_number',
        label='Machine Serial Number',
        widget=forms.Select()
    )
    machine_model = django_filters.ModelChoiceFilter(
        queryset=MachineModelReference.objects.all(),
        field_name='machine__model',
        label='Machine Model',
        widget=forms.Select()
    )
    engine_model = django_filters.ModelChoiceFilter(
        queryset=EngineModelReference.objects.all(),
        field_name='machine__engine_model',
        label='Engine Model',
        widget=forms.Select()
    )
    transmission_model = django_filters.ModelChoiceFilter(
        queryset=TransmissionModelReference.objects.all(),
        field_name='machine__transmission_model',
        label='Transmission Model',
        widget=forms.Select()
    )
    steer_axel_model = django_filters.ModelChoiceFilter(
        queryset=SteerAxleModelReference.objects.all(),
        field_name='machine__steer_axle_model',
        label='Steer Axle Model',
        widget=forms.Select()
    )
    drive_axel_model = django_filters.ModelChoiceFilter(
        queryset=DriveAxleModelReference.objects.all(),
        field_name='machine__drive_axle_model',
        label='Drive Axle Model',
        widget=forms.Select()
    )
    maintenance_type = django_filters.ModelChoiceFilter(
        queryset=TechnicalMaintenanceTypeReference.objects.all(),
        label='Maintenance Type',
        widget=forms.Select()
    )
    maintenance_date = django_filters.DateFilter(
        field_name='maintenance_date',
        lookup_expr='exact',
        label='Maintenance Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    order_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Order Number',
        widget=forms.TextInput()
    )
    order_date = django_filters.DateFilter(
        field_name='order_date',
        lookup_expr='exact',
        label='Order Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    service_company = django_filters.ModelChoiceFilter(
        queryset=ServiceCompanyReference.objects.all(),
        label='Service Company',
        widget=forms.Select()
    )

    class Meta:
        model = TechnicalMaintenance
        fields = [
            'serial_number', 'machine_model', 'engine_model',
            'transmission_model', 'steer_axel_model',
            'drive_axel_model', 'maintenance_type',
            'maintenance_date', 'order_number',
            'order_date', 'service_company'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        user_groups = user.groups.values_list('id', flat=True)

        if 4 in user_groups:
            self.filters['serial_number'].queryset = Machine.objects.filter(client=user)
        else:
            self.filters['serial_number'].queryset = Machine.objects.all()