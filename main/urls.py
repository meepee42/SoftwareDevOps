from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('delete/<int:location_id>', views.delete, name='delete'),
    path('location/<int:location_id>', views.location, name='location'),

    path('location/create/<int:location_id>', views.createcharger, name='createcharger'),
    path('location/delete/<int:charger_id>', views.deletecharger, name='deletecharger'),
    path('location/charger/<int:charger_id>', views.charger, name='charger'),
    path('users/', views.users, name='users'),
    path('register/', views.register, name='register'),
    path('users/delete/<int:user_id>', views.userdelete, name='userdelete'),
    path('users/admin/<int:user_id>', views.useradmin, name='useradmin'),

]