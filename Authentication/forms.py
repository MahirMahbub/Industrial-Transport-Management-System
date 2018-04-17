from django.contrib.auth.forms import UserCreationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from Authentication.models import Address, Vehicle, UserProfile
# from bootstrap_datepicker.widgets import DatePicker
from django.contrib.admin import widgets

from ITMS_Project_Final import settings


class DateInput(forms.DateInput):
    input_type = 'date'

class CurrentAddressForm(forms.ModelForm):
    CHOICES = [('client', 'Client'),
               ('owner', 'Owner')]

    user_type = forms.ChoiceField( choices=CHOICES, widget=forms.RadioSelect() )
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=100)
    district = forms.CharField(max_length=200)
    sub_district = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    zip = forms.IntegerField()
    #p_address = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Address
        fields =('user_type','phone_number', 'zip', 'district', 'sub_district','city',)

class PermanentAddressForm(forms.ModelForm):
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    CHOICES = [('client', 'Client'),
               ('owner', 'Owner')]

    user_type = forms.ChoiceField( choices=CHOICES, widget=forms.RadioSelect() )
    phone_number = forms.CharField(max_length=100)
    district = forms.CharField( max_length=200 )
    sub_district = forms.CharField( max_length=200 )
    city = forms.CharField( max_length=200 )
    zip = forms.IntegerField()

    # p_address = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Address
        fields = '__all__'


class AddVehicleForm(forms.ModelForm):
    license_no = forms.CharField(max_length=200)
    chassis_no = forms.CharField(max_length=200)
    journey_date = forms.DateField(widget=forms.SelectDateWidget())
    #DateInput( attrs={'size': '15', 'id': 'datepicker', 'readonly': 'readonly'} ))
    # p_address = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Vehicle
        fields = ('license_no', 'chassis_no', 'journey_date', 'capacity', 'model',)
        # widgets = {
        #     'journey_date': forms.DateTimeInput( attrs={'class': 'datetime-input'} )
        # }
