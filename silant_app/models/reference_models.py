# reference_models.py

from django.db import models

class MachineModelReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class EngineModelReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class TransmissionModelReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class DriveAxleModelReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class SteerAxleModelReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class ServiceCompanyReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class TechnicalMaintenanceTypeReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class FailureUnitReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name


class RecoveryMethodReference(models.Model):
    name = models.CharField(max_length=255)
    specification = models.TextField()

    def __str__(self):
        return self.name
