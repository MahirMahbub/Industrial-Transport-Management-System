from django.contrib.auth.forms import UserCreationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from Authentication.models import Address


class CurrentAddressForm(forms.ModelForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=100)
    district = forms.CharField(max_length=200)
    sub_district = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    zip = forms.IntegerField()
    #p_address = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Address
        fields = '__all__'

class PermanentAddressForm(forms.ModelForm):
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=100)
    district = forms.CharField( max_length=200 )
    sub_district = forms.CharField( max_length=200 )
    city = forms.CharField( max_length=200 )
    zip = forms.IntegerField()

    # p_address = forms.ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = Address
        fields = '__all__'
