from time import strftime

from django.test import TestCase
from main.models import CouncilLocations, VehicleChargingStation
import datetime


# Create your tests here.

class ModelsTest(TestCase):
    def setUp(self):
        CouncilLocations.objects.create(id=1, locationName="Test Location", addressLine1="Test Address",
                                        addressLine2="Test Address 2", postcode="Test Postcode")
        CouncilLocations.objects.create(locationName="Test Location", addressLine1="Test Address",
                                        addressLine2="Test Address 2", postcode="Test Postcode")
        VehicleChargingStation.objects.create(id=1, councilLocation_id=1, chargingStationName="Test Charger",
                                              installedDate=datetime.datetime(2026,6,1), lastReviewDate=datetime.datetime(2026,6,1),
                                              nextReviewDate=datetime.datetime(2027,6,1), powerOutput=130)

    def testCouncilLocationsModel(self):

        location = CouncilLocations.objects.get(id=1)
        self.assertEqual(location.locationName, "Test Location")
        self.assertEqual(CouncilLocations.objects.filter(id=1).count(), 1)
        self.assertEqual(CouncilLocations.objects.count(), 2)

    def testVehicleChargingStationModel(self):
        chargingstation = VehicleChargingStation.objects.get(id=1)
        self.assertEqual(chargingstation.chargingStationName, "Test Charger")
        self.assertEqual(VehicleChargingStation.objects.filter(id=1).count(), 1)




