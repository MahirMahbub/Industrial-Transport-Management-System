from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Address(models.Model):

    district = models.CharField(max_length=200, default="Dhaka")
    sub_district = models.CharField(max_length=200, default="Dhaka")
    city = models.CharField(max_length=200, default="Dhaka")
    zip = models.IntegerField(default=1000)
    phone_number = models.CharField(max_length=100, null=True)


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
    journey_date = models.DateField()
    capacity = models.FloatField(default=0.0)
    model = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class UserProfile(models.Model):
    user =  models.OneToOneField(User, related_name="profile", on_delete = models.CASCADE)
    permanent_address =  models.OneToOneField(Address, related_name="permanent", on_delete = models.CASCADE)
    current_address = models.OneToOneField(Address, related_name="current", on_delete = models.CASCADE)
