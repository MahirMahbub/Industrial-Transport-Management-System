import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Address(models.Model):

    district = models.CharField(max_length=200, default="Dhaka")
    sub_district = models.CharField(max_length=200, default="Dhaka")
    city = models.CharField(max_length=200, default="Dhaka")
    zip = models.IntegerField(default=1000)
    phone_number = models.CharField(max_length=100, null=True)
    user = models.OneToOneField( User, on_delete=models.CASCADE, null = True)


# class CurrentAddress(models.Model):
#     district = models.CharField(max_length=200, default="Dhaka")
#     sub_distict = models.CharField(max_length=200, default="Dhaka")
#     city = models.CharField(max_length=200, default="Dhaka")
#     zip = models.IntegerField(default=1000)
#     user = models.ForeignKey( User, on_delete=models.CASCADE )

# class Client(models.Model):
#     client_name = models.CharField( max_length=200 )
#     # permanent_address = models.ForeignKey( PermanentAddress, on_delete=models.CASCADE, default=1 )
#
#     # current_address = models.ForeignKey( CurrentAddress, on_delete=models.CASCADE, default=1 )
#     email = models.EmailField()
#     password = models.CharField( max_length=200 )
#
# @receiver(post_save, sender=User)
# def update_client_profile(sender, instance, created, **kwargs):
#     if created:
#         Client.objects.create(user=instance)
#     instance.profile.save()

# class Owner(models.Model):
#     Owner_name = models.CharField( max_length=200 )
#     permanent_address = models.ForeignKey( PermanentAddress, on_delete=models.CASCADE, default=1 )
#
#     current_address = models.ForeignKey( CurrentAddress, on_delete=models.CASCADE, default=1 )
#     email = models.EmailField()
#     password = models.CharField( max_length=200 )


class Vehicle(models.Model):
    #vehicle_id = models.BigAutoField(primary_key=True)
    license_no = models.CharField(max_length=200)
    chassis_no = models.CharField(max_length=200)
    journey_date = models.DateField(default=datetime.date.today, null=True)
    capacity = models.FloatField(default=0.0,  help_text = 'Capacity in Ton')
    model = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    driver_code_name = models.OneToOneField( User, on_delete=models.CASCADE,related_name="driver_code", null = True)
    client = models.ForeignKey(User, on_delete=models.CASCADE,related_name="client", null=True)
    place = models.CharField(max_length=200, null=True)

    def get_absolute_url_borrowed(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        print( reverse( 'Borrowed_vehicle_detail_view', args=[str( self.id )] ) )
        return reverse( 'Borrowed_vehicle_detail_view', args=[str( self.id )] )

    def get_absolute_url_borrow(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        print(reverse( 'borrow_vehicle_details_view', args=[str( self.id )] ))
        return reverse( 'borrow_vehicle_details_view', args=[str( self.id )] )

    def get_absolute_url_added(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        print(reverse( 'added_vehicle_detail_view', args=[str( self.id )] ))
        return reverse( 'added_vehicle_detail_view', args=[str( self.id )] )

    def get_absolute_url_show(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        print(reverse( 'get_loc_data', args=[str( self.id )] ))
        return reverse( 'get_loc_data', args=[str( self.id )] )

# class BookVehicle(models.Model):
#     client = models.OneToOneField( User, on_delete=models.CASCADE,related_name="driver_code", null = True)
#     ve
class UserProfile(models.Model):
    user =  models.OneToOneField(User, related_name="profile", on_delete = models.CASCADE)
    permanent_address =  models.OneToOneField(Address, related_name="permanent", on_delete = models.CASCADE)
    current_address = models.OneToOneField(Address, related_name="current", on_delete = models.CASCADE)

class TrackVehicle(models.Model):
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null= True)
    this_vehicle = models.OneToOneField(Vehicle, related_name="this_vehicle", on_delete = models.CASCADE, null=True)
    time = models.CharField(null=True, max_length=200)
    def get_absolute_url_show(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        print( reverse( 'get_loc_data', args=[str( self.id )] ) )
        return reverse( 'get_loc_data', args=[str( self.id )] )

class LocationVehicle(models.Model):
    destination = models.CharField(null = True, max_length=200)
    middle_place = models.CharField(null=True, max_length=200)
    start_place = models.CharField(null=True, max_length=200)
    vehicle = models.OneToOneField(Vehicle, related_name="vehicle", on_delete = models.CASCADE)
