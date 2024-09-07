from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import Group
from .models.models import CustomUser, Machine, TechnicalMaintenance, Claim
from .models.reference_models import (
    MachineModelReference, EngineModelReference, TransmissionModelReference,
    DriveAxleModelReference, SteerAxleModelReference, ServiceCompanyReference,
    TechnicalMaintenanceTypeReference, FailureUnitReference, RecoveryMethodReference
)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_service_company', 'is_staff', 'is_active']
    list_filter = ['is_service_company', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'is_service_company')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_service_company', 'is_staff', 'is_active', 'groups')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group)
admin.site.register(Machine)
admin.site.register(TechnicalMaintenance)
admin.site.register(Claim)
admin.site.register(MachineModelReference)
admin.site.register(EngineModelReference)
admin.site.register(TransmissionModelReference)
admin.site.register(DriveAxleModelReference)
admin.site.register(SteerAxleModelReference)
admin.site.register(ServiceCompanyReference)
admin.site.register(TechnicalMaintenanceTypeReference)
admin.site.register(FailureUnitReference)
admin.site.register(RecoveryMethodReference)