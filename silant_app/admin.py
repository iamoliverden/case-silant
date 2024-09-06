from django.contrib import admin
from .models.models import *


@admin.register(MachineModelReference)
class MachineModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(EngineModelReference)
class EngineModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(TransmissionModelReference)
class TransmissionModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(DriveAxleModelReference)
class DriveAxleModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(SteerAxleModelReference)
class SteerAxleModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(ServiceCompanyReference)
class ServiceCompanyReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(TechnicalMaintenanceTypeReference)
class TechnicalMaintenanceTypeReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(FailureUnitReference)
class FailureUnitReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(RecoveryMethodReference)
class RecoveryMethodReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'specification')


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'serial_number', 'model', 'engine_model', 'transmission_model', 'drive_axle_model', 'steer_axle_model',
        'shipment_date', 'client', 'service_company')


@admin.register(TechnicalMaintenance)
class TechnicalMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'operating_hours', 'order_number', 'order_date',
                    'service_company')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        'machine', 'failure_date', 'operating_hours', 'failure_unit', 'recovery_method', 'recovery_date', 'downtime',
        'service_company')
