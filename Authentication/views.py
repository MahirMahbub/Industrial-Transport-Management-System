from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Authentication.forms import CurrentAddressForm, PermanentAddressForm, AddVehicleForm
from Authentication.models import Address, UserProfile, Vehicle


# def index(request):
#     return render_to_response("base.html",
#                               RequestContext(request))

# Create your views here.
@login_required
def address_view(request):
    # if this is a POST request we need to process the form data
    # cur_form,per_form = 0,0
    cur_form = 0
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        cur_form = CurrentAddressForm(request.POST)
        # per_form = PermanentAddressForm(request.POST)
        # check whether it's valid:
        if cur_form.is_valid():
            #current address form reading
            # profile = UserProfile(user = request.user)

            phone_number = cur_form.cleaned_data['phone_number']
            district = cur_form.cleaned_data['district']
            sub_district = cur_form.cleaned_data['sub_district']
            city = cur_form.cleaned_data['city']
            zip = cur_form.cleaned_data['zip']
            user_type = cur_form.cleaned_data['user_type']
            print(user_type)
            print("Working it")
            print(district)
            user_profile = None
            if request.user.is_authenticated():
                user_profile = request.user
                # if request.user.is_authenticated():
                #     user = request.user
            if str(user_type) == 'client':
                user_profile  =  request.user
                group = Group.objects.get( name='Client' )
                user_profile .groups.add( group )
            else:
                user_profile  =  request.user
                group = Group.objects.get( name='Owner' )
                user_profile .groups.add( group )
            current_address = Address.objects.create(district=district, sub_district=sub_district, city=city, zip=zip,phone_number =  phone_number)
            user_profile.current_address = current_address
            #
            #
            # phone_number = per_form.cleaned_data['phone_number']
            # district = per_form.cleaned_data['district']
            # sub_district = per_form.cleaned_data['sub_district']
            # city = per_form.cleaned_data['city']
            # zip = per_form.cleaned_data['zip']
            # permanent_address = Address.objects.create( district=district, sub_district=sub_district, city=city, zip=zip,phone_number = phone_number )
            # print(district)
            # profile.permanent_address = permanent_address
            # profile.save()

        else:
            cur_form = CurrentAddressForm()
            # per_form = CurrentAddressForm()



        return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        cur_form = CurrentAddressForm()
        # per_form  = PermanentAddressForm()

    return render(request, 'AddressFormSheet.html', {'cur_form': cur_form})


def add_vehicle_view(request):
    if request.method == 'POST':
        add_veh = AddVehicleForm(request.POST)
        if add_veh.is_valid():
            license_no = add_veh.cleaned_data['license_no']
            chassis_no = add_veh.cleaned_data['chassis_no']
            journey_date = add_veh.cleaned_data['journey_date']
            capacity = add_veh.cleaned_data['capacity']
            model = add_veh.cleaned_data['model']
            print("Time")
            user_profile = None
            # if request.user.is_authenticated():
            user_profile = request.user
            #print(journey_date)
            vehicle = Vehicle.objects.create( license_no = license_no, chassis_no = chassis_no,
                                              journey_date=journey_date,capacity=capacity, model=model)
            vehicle.user = user_profile
            vehicle.save()
        return HttpResponseRedirect( '/accounts/add_vehicle' )
    else:
        add_veh = AddVehicleForm()

    return  render(request, 'AddVehicleFormSheet.html', {'add_veh': add_veh})


def dummy(request):
    # user = User.objects.get(username='user1')
    # #user = request.user
    # txt = "<h2>"
    # txt += "username: " + user.username
    # txt += "present address City: " + user.profile.current_address.city
    # txt += "permnent district: "  + user.profile.permanent_address.district + "</h2>"
    # return HttpResponse("Welcoome")
    # return render_to_response( "base.html",
    #                            RequestContext( request ) )
    return render( request, 'allauth/account/home.html' )