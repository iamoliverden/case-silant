# models.py

from django.conf import settings
from .reference_models import *
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_service_company = models.BooleanField(default=False)


# Machine Model
class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    model = models.ForeignKey(MachineModelReference, related_name='machine_models', on_delete=models.CASCADE)
    engine_model = models.ForeignKey(EngineModelReference, related_name='engine_models', on_delete=models.CASCADE)
    engine_serial_number = models.CharField(max_length=255)
    transmission_model = models.ForeignKey(TransmissionModelReference, related_name='transmission_models',
                                           on_delete=models.CASCADE)
    transmission_serial_number = models.CharField(max_length=255)
    drive_axle_model = models.ForeignKey(DriveAxleModelReference, related_name='drive_axle_models',
                                         on_delete=models.CASCADE)
    drive_axle_serial_number = models.CharField(max_length=255)
    steer_axle_model = models.ForeignKey(SteerAxleModelReference, related_name='steer_axle_models',
                                         on_delete=models.CASCADE)
    steer_axle_serial_number = models.CharField(max_length=255)
    supply_contract = models.CharField(max_length=255)
    shipment_date = models.DateField()
    consignee = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    configuration = models.TextField(max_length=255)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='machines', on_delete=models.SET_NULL, null=True,
                               blank=True)
    service_company = models.ForeignKey(ServiceCompanyReference, related_name='service_companies',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.serial_number


# Technical Maintenance Model
class TechnicalMaintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    maintenance_type = models.ForeignKey(TechnicalMaintenanceTypeReference, related_name='maintenance_types',
                                         on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    operating_hours = models.IntegerField()
    order_number = models.CharField(max_length=255)
    order_date = models.DateField()
    service_company = models.ForeignKey(ServiceCompanyReference, related_name='maintenance_service_companies',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.maintenance_type} - {self.machine.serial_number}"


# Claims Model
class Claim(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    failure_date = models.DateField()
    operating_hours = models.IntegerField()
    failure_unit = models.ForeignKey(FailureUnitReference, related_name='failure_units', on_delete=models.CASCADE)
    failure_description = models.TextField()
    recovery_method = models.ForeignKey(RecoveryMethodReference, related_name='recovery_methods',
                                        on_delete=models.CASCADE)
    used_spare_parts = models.TextField()
    recovery_date = models.DateField()
    downtime = models.IntegerField()  # Calculated as recovery_date - failure_date
    service_company = models.ForeignKey(ServiceCompanyReference, related_name='claim_service_companies',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return f"Claim for {self.machine.serial_number} on {self.failure_date}"
