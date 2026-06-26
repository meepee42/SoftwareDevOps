from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    admin = models.BooleanField(default=False)

# Create your models here.
class CouncilLocations(models.Model):
    locationName = models.CharField(max_length=120)
    addressLine1 = models.CharField(max_length=120)
    addressLine2 = models.CharField(max_length=120)
    postcode = models.CharField(max_length=120)

    def __str__(self):
        return self.locationName

class VehicleChargingStation(models.Model):
    councilLocation = models.ForeignKey(CouncilLocations, on_delete=models.CASCADE)
    chargingStationName = models.CharField(max_length=120)
    installedDate = models.DateField()
    lastReviewDate = models.DateField()
    nextReviewDate = models.DateField()
    powerOutput = models.IntegerField()

    def __str__(self):
        return self.chargingStationName

