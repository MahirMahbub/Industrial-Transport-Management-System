from django.http import HttpResponseRedirect
from django.shortcuts import render
from Authentication.forms import CurrentAddressForm,PermanentAddressForm
from Authentication.models import Address, UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def address_view(request):
    # if this is a POST request we need to process the form data
    cur_form,per_form = 0,0
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        cur_form = CurrentAddressForm(request.POST)
        per_form = PermanentAddressForm(request.POST)
        # check whether it's valid:
        if cur_form.is_valid() and per_form.is_valid():
            #current address form reading
            profile = UserProfile(user = request.user)
            #profile = request.user
            print(profile)
            phone_number = cur_form.cleaned_data['phone_number']
            district = cur_form.cleaned_data['district']
            sub_district = cur_form.cleaned_data['sub_district']
            city = cur_form.cleaned_data['city']
            zip = cur_form.cleaned_data['zip']
            print("Working it")
            print(district)
            current_address = Address.objects.create(district=district, sub_district=sub_district, city=city, zip=zip,phone_number =  phone_number)
            profile.current_address = current_address


            phone_number = per_form.cleaned_data['phone_number']
            district = per_form.cleaned_data['district']
            sub_district = per_form.cleaned_data['sub_district']
            city = per_form.cleaned_data['city']
            zip = per_form.cleaned_data['zip']
            permanent_address = Address.objects.create( district=district, sub_district=sub_district, city=city, zip=zip,phone_number = phone_number )
            print(district)
            profile.permanent_address = permanent_address
            profile.save()

        else:
            cur_form = PermanentAddressForm()
            per_form = CurrentAddressForm()



        return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        cur_form = CurrentAddressForm()
        per_form  = PermanentAddressForm()

    return render(request, 'AddressFormSheet.html', {'cur_form': cur_form, 'per_form': per_form})

from django.shortcuts import HttpResponse
from django.contrib.auth.models import User

def dummy(request):
    # user = User.objects.get(username='user1')
    # #user = request.user
    # txt = "<h2>"
    # txt += "username: " + user.username
    # txt += "present address City: " + user.profile.current_address.city
    # txt += "permnent district: "  + user.profile.permanent_address.district + "</h2>"
    return HttpResponse("Welcoome")