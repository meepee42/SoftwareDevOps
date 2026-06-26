from django import  forms
from django.contrib.auth import  login,authenticate
from django.contrib.auth.forms import UserCreationForm
from main.models import User

class CreateNewLocation(forms.Form):
    LocationName = forms.CharField(label="Location", max_length=100)
    addressLine1 = forms.CharField(label="Address Line 1", max_length=100)
    addressLine2 = forms.CharField(label="Address Line 2", max_length=100)
    postcode = forms.CharField(label="Postcode", max_length=100)

class ChargingStationForm(forms.Form):
    chargingStationName = forms.CharField(label="Name", max_length=100)
    installedDate = forms.DateField(label="Installed Date", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    lastReviewDate = forms.DateField(label="Last Review Date", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    nextReviewDate = forms.DateField(label="Next Review Date", widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    powerOutput = forms.IntegerField(label="Power Output (kW)", min_value=0, max_value=1000)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Contact Email", max_length=100)
    admin = forms.BooleanField(label="Is Admin?", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "admin")

class SelfRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Contact Email", max_length=100)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

