from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import CouncilLocations, VehicleChargingStation, User
from .forms import CreateNewLocation, ChargingStationForm, RegistrationForm, SelfRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser
from django.contrib import messages

# Create your views here.
def index(response):
    locations = CouncilLocations.objects.all()
    return render(response, "main/index.html", {"locations": locations})

def create(response):
    if response.method == "POST":
        form = CreateNewLocation(response.POST)
        if response.user.admin:
            if form.is_valid():
                location = form.cleaned_data["LocationName"]
                address1 = form.cleaned_data["addressLine1"]
                address2 = form.cleaned_data["addressLine2"]
                postcode = form.cleaned_data["postcode"]
                newlocation = CouncilLocations(locationName=location, addressLine1=address1, addressLine2=address2,
                                               postcode=postcode)
                newlocation.save()
                messages.add_message(response, messages.SUCCESS, 'Location Added')
                return HttpResponseRedirect("/location/%i" % newlocation.id)
                # return HttpResponseRedirect("/")
        else:
            messages.add_message(response, messages.ERROR, 'You do not have the permissions to delete this location')

    else:
        form = CreateNewLocation()
    return render(response, "main/create.html", {"form": form})

def delete(response, location_id):
    if response.user.admin:
        councillocations = CouncilLocations.objects.get(id=location_id)
        locationChargingStation = VehicleChargingStation.objects.filter(councilLocation_id=location_id)
        for chargingstation in locationChargingStation:
            chargingstation.delete()
        councillocations.delete()
        messages.add_message(response, messages.SUCCESS, 'Location Deleted')
    else:
        messages.add_message(response, messages.ERROR, 'You do not have the permissions to delete this location')
    return HttpResponseRedirect("/")

def location(response, location_id):
    ls = CouncilLocations.objects.get(id=location_id)
    chargers  = ls.vehiclechargingstation_set.all()
    if response.method == "POST":
        form = CreateNewLocation(response.POST)
        if form.is_valid():
            locationname = form.cleaned_data["LocationName"]
            address1 = form.cleaned_data["addressLine1"]
            address2 = form.cleaned_data["addressLine2"]
            postcode = form.cleaned_data["postcode"]
            updatedlocation = CouncilLocations(id=ls.id ,locationName=locationname, addressLine1=address1, addressLine2=address2, postcode=postcode)
            updatedlocation.save()
            messages.add_message(response, messages.SUCCESS, 'Location updated')
            return HttpResponseRedirect("/location/%i"  %ls.id)
    else:
        initial_data = {
            'LocationName': ls.locationName,
            'addressLine1': ls.addressLine1,
            'addressLine2': ls.addressLine2,
            'postcode': ls.postcode,
        }
        form = CreateNewLocation(initial_data)
        if  not response.user.admin:
            form.fields['LocationName'].widget.attrs['readonly']  = True
            form.fields['addressLine1'].widget.attrs['readonly'] = True
            form.fields['addressLine2'].widget.attrs['readonly'] = True
            form.fields['postcode'].widget.attrs['readonly'] = True
    return render(response, "main/location.html", {"form": form, "ls": ls, "chargers":chargers})

def createcharger(response, location_id):
    if response.method == "POST":
        form = ChargingStationForm(response.POST)
        if form.is_valid():
            chargingstationname = form.cleaned_data["chargingStationName"]
            installeddate = form.cleaned_data["installedDate"]
            lastreviewdate = form.cleaned_data["lastReviewDate"]
            nextreviewdate = form.cleaned_data["nextReviewDate"]
            poweroutput = form.cleaned_data["powerOutput"]
            newcharger = VehicleChargingStation(councilLocation_id=location_id, chargingStationName=chargingstationname, installedDate=installeddate, lastReviewDate=lastreviewdate, nextReviewDate=nextreviewdate, powerOutput=poweroutput)
            newcharger.save()
            messages.add_message(response, messages.SUCCESS, 'Charger Added')
            return HttpResponseRedirect("/location/%i"  %location_id)
            #return HttpResponseRedirect("/")
    else:
        form = ChargingStationForm()
        return render(response, "main/createcharger.html", {"form": form, "location_id": location_id})

def deletecharger(response, charger_id):
    charger = VehicleChargingStation.objects.get(id=charger_id)
    location_id = charger.councilLocation_id
    charger.delete()
    messages.add_message(response, messages.SUCCESS, 'Charger Deleted')
    return HttpResponseRedirect("/location/%i" %location_id)

def charger(response, charger_id):
    charger = VehicleChargingStation.objects.get(id=charger_id)
    if response.method == "POST":
        form = ChargingStationForm(response.POST)
        if form.is_valid():
            chargingstationname = form.cleaned_data["chargingStationName"]
            installeddate = form.cleaned_data["installedDate"]
            lastreviewdate = form.cleaned_data["lastReviewDate"]
            nextreviewdate = form.cleaned_data["nextReviewDate"]
            poweroutput = form.cleaned_data["powerOutput"]
            updatedcharger = VehicleChargingStation(id=charger.id, chargingStationName=chargingstationname,installedDate=installeddate, lastReviewDate=lastreviewdate, nextReviewDate=nextreviewdate, powerOutput=poweroutput, councilLocation_id=charger.councilLocation_id)
            updatedcharger.save()
            messages.add_message(response, messages.SUCCESS, 'Charger Updated')
            return HttpResponseRedirect("/location/charger/%i" % charger.id)
    else:
        initial_data = {
            'chargingStationName': charger.chargingStationName,
            'installedDate': charger.installedDate,
            'lastReviewDate': charger.lastReviewDate,
            'nextReviewDate': charger.nextReviewDate,
            'powerOutput': charger.powerOutput,
        }
        form = ChargingStationForm(initial_data)
    return render(response, "main/charger.html", {"form": form, "charger_id":charger_id, "location_id": charger.councilLocation_id})

def users(response):
    if response.user.is_authenticated:
        if response.user.admin:
            accounts = User.objects.all()
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
    return render(response, "main/users.html", {"accounts": accounts})

def register(response):
    if response.user.is_authenticated:
        if response.user.admin:
            if response.method == "POST":
                form = RegistrationForm(response.POST)
                if form.is_valid():
                    form.save()
                    messages.add_message(response, messages.SUCCESS, 'User registered')
                    return HttpResponseRedirect("/users")
            else:
                form = RegistrationForm()
        else:
            return HttpResponseRedirect("/")
    else:
        if response.method == "POST":
            form = SelfRegistrationForm(response.POST)
            if form.is_valid():
                form.save()
                messages.add_message(response, messages.SUCCESS, 'Account Created')
                return HttpResponseRedirect("/")
        else:
            form = SelfRegistrationForm()
    return render(response, "main/register.html", {"form": form})

def userdelete(response, user_id):
    if response.user.is_authenticated:
        if response.user.admin:
            if User.objects.count() == 1:
                messages.add_message(response, messages.ERROR,'Unable to delete. Would result in 0 users')
            else:
                selecteduser = User.objects.get(id=user_id)
                adminCount = User.objects.filter(admin=True).count()
                if selecteduser.admin == True and adminCount == 1:
                    messages.add_message(response, messages.ERROR, 'Unable to delete. Would result in 0 admins' )
                else:
                    selecteduser.delete()
                    messages.add_message(response, messages.SUCCESS, 'User Deleted')

        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/users")

def useradmin(response, user_id):
    if response.user.is_authenticated:
        if response.user.admin:
            selecteduser = User.objects.get(id=user_id)
            if selecteduser.admin:
                adminCount = User.objects.filter(admin=True).count()
                if adminCount == 1:
                    messages.add_message(response, messages.ERROR, 'Unable to change admin status. Would result in 0 admins')
                    return HttpResponseRedirect("/users")
                else:
                    selecteduser.admin = False
            else:
                selecteduser.admin = True
            selecteduser.save()
            messages.add_message(response, messages.SUCCESS, 'Admin status updated')
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
    return HttpResponseRedirect("/users")

