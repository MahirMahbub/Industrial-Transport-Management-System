import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DeleteView

from Authentication.forms import CurrentAddressForm, PermanentAddressForm, AddVehicleForm,DriverLogin, BorrowVehicleForm
from Authentication.models import Address, UserProfile, Vehicle
from django.contrib.auth import logout, authenticate, login


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
            if request.user.is_authenticated:
                #user_profile = UserProfile( user=request.user )
                user_profile = request.user
                # if request.user.is_authenticated():
                #     user = request.user
                if str(user_type) == 'client':
                    #user_profile  =  request.user
                    group = Group.objects.get( name='Client' )
                    user_profile .groups.add( group )
                else:
                    #user_profile  =  request.user
                    group = Group.objects.get( name='Owner' )
                    user_profile .groups.add( group )
            current_address = Address.objects.create(district=district, sub_district=sub_district, city=city, zip=zip,phone_number =  phone_number)
            #user_profile.current_ = current_address
            current_address.user = user_profile
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
            driver_code = add_veh.cleaned_data['driver_code']
            #journey_date = add_veh.cleaned_data['journey_date']
            capacity = add_veh.cleaned_data['capacity']
            model = add_veh.cleaned_data['model']
            passwd_veh = add_veh.cleaned_data['vehicle_password']
            passwd_hashed = make_password(str(passwd_veh))
            print("Time")
            user_profile = None
            # if request.user.is_authenticated():
            # user_profile = request.userauth_group_permissions
            user_profile = request.user
            #print(journey_date)
            vehicle = Vehicle.objects.create( license_no = license_no, chassis_no = chassis_no,
                                              journey_date=datetime.date.today(),capacity=capacity, model=model)
            vehicle.user = user_profile
            group = Group.objects.get( name='Driver' )

            driver_user = User.objects.create( username= driver_code, password=passwd_hashed,is_active= True)
            # vehicle.driver_code_name.username = driver_code
            # vehicle.driver_code_name.password = passwd_veh
            # vehicle.driver_code_name.is_active = True
            vehicle.driver_code_name = driver_user
            driver_user.groups.add( group )
            driver_user.save()
            vehicle.save()
        return HttpResponseRedirect( '/accounts/add_vehicle' )
    else:
        add_veh = AddVehicleForm()

    return  render(request, 'AddVehicleFormSheet.html', {'add_veh': add_veh})


def borrow_vehicle_view(request):
    borr_veh = None
    if request.method == 'POST':
        borr_veh = BorrowVehicleForm(request.POST)
        if borr_veh.is_valid():
            journey_date = borr_veh.cleaned_data['journey_date']
            capacity = borr_veh.cleaned_data['capacity']
            request.session['capacity'] = float(capacity)
            request.session['journey_date'] = str(journey_date)
            print(journey_date)
            print("Time")
            # user_profile = None
            # if request.user.is_authenticated():
            #   user_profile = request.user
            # print(journey_date)
            # vehicle = Vehicle.objects.create( license_no = license_no, chassis_no = chassis_no,
            #                                   journey_date=journey_date,capacity=capacity, model=model)
            # vehicle.user = user_profile
            # vehicle.save()
        return HttpResponseRedirect( '/accounts/borrow_vehicle_list' )
    else:
        borr_veh = BorrowVehicleForm()

    return  render(request, 'BorrowVehicleFormSheet.html', {'borr_veh': borr_veh})

def borrow_vehicle_list_view(request):
    _capacity = request.session.get('capacity')
    _journey_date = request.session.get('journey_date')
    borrow_vehicle_list = Vehicle.objects.filter( capacity__gte= _capacity ).exclude(journey_date__lte=_journey_date)
    page = request.GET.get('page', 1)
    #borrow_vehicle = None
    paginator = Paginator(borrow_vehicle_list,2)
    try:
        borrow_vehicle = paginator.page(page)
    except PageNotAnInteger:
        borrow_vehicle = paginator.page(1)
    except EmptyPage:
        borrow_vehicle = paginator.page(paginator.num_pages)
    return render( request, 'BorrowVehicleListSheet.html', {'borrow_vehicle': borrow_vehicle} )

def borrow_vehicle_details_view(request, pk):

    try:
        vehicle = Vehicle.objects.get( pk=pk )
    except Vehicle.DoesNotExist:
        raise Http404( "Book does not exist" )
    try:
        if request.method == 'POST' and request.POST['book'] == 'Confirm':
            veh = Vehicle.objects.get( pk=pk )
            if not veh.client:
                veh.client = request.user
                veh.save()
                return HttpResponse("Booked")
            else:
                return HttpResponse( 'Can not Book.Already Booked')
    except MultiValueDictKeyError:
            HttpResponse("Internal Error")

    # book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'BorrowVehicleDetails.html',
        context={'vehicle': vehicle, }
    )


def driver_login(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        driv_log_in = DriverLogin(request.POST)
        if driv_log_in.is_valid():
            driver_code = driv_log_in.cleaned_data['driver_code']
            passwd_veh = driv_log_in.cleaned_data['vehicle_password']
            #passwd_hashed = make_password(str(passwd_veh))
            user = User.objects.get( username=driver_code )
            #user = authenticate( username=driver_code, password=passwd_veh )
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login( request, user)
        return HttpResponseRedirect( '/' )
    else:
        driv_log_in = DriverLogin()

    return render( request, 'DriverLogin.html', {'form': driv_log_in} )

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
#
# class AuthorDelete(DeleteView):
#     model = Vehicle
#     success_url = reverse_lazy('borrow_vehicle_details_view')

def added_vehicle_list_view(request):
    user = request.user
    added_vehicle_list = Vehicle.objects.filter( user= user )
    page = request.GET.get('page', 1)
    #borrow_vehicle = None
    paginator = Paginator(added_vehicle_list,2)
    try:
        added_vehicle = paginator.page(page)
    except PageNotAnInteger:
        added_vehicle = paginator.page(1)
    except EmptyPage:
        added_vehicle = paginator.page(paginator.num_pages)
    return render( request, 'AddVehiceListSheet.html', {'added_vehicle': added_vehicle} )

def added_vehicle_details_view(request, pk):

    try:
        vehicle = Vehicle.objects.get( pk=pk )
    except Vehicle.DoesNotExist:
        raise Http404( "Book does not exist" )
    try:
        if request.method == 'POST' and request.POST['delete'] == 'Delete':
            veh = Vehicle.objects.get( pk=pk )
            veh.delete()
            return HttpResponse( 'deleted' )
    except MultiValueDictKeyError:
        HttpResponse("Internal Error")

    # book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'AddedVehicleDetails.html',
        context={'vehicle': vehicle, }
    )
