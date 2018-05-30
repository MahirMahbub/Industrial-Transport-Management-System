import datetime
import json
from django.contrib import messages
from permission import group_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext, context
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DeleteView

from Authentication.forms import CurrentAddressForm, PermanentAddressForm, AddVehicleForm,DriverLogin, BorrowVehicleForm
from Authentication.models import Address, UserProfile, Vehicle, TrackVehicle, LocationVehicle
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
            current_address.save()
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

@login_required
@group_required('Owner')
def add_vehicle_view(request):
    if request.method == 'POST':
        add_veh = AddVehicleForm(request.POST)
        if add_veh.is_valid():
            try:
                license_no = add_veh.cleaned_data['license_no']
                chassis_no = add_veh.cleaned_data['chassis_no']
                driver_code = add_veh.cleaned_data['driver_code']
                #journey_date = add_veh.cleaned_data['journey_date']
                capacity = add_veh.cleaned_data['capacity']
                model = add_veh.cleaned_data['model']
                passwd_veh = add_veh.cleaned_data['vehicle_password']
                place = add_veh.cleaned_data["place"]
                passwd_hashed = make_password(str(passwd_veh))
                print("Time")
                user_profile = None
                # if request.user.is_authenticated():
                # user_profile = request.userauth_group_permissions
                user_profile = request.user
                #print(journey_date)
                vehicle = Vehicle.objects.create( license_no = license_no, chassis_no = chassis_no,
                                                  journey_date=datetime.date.today(),capacity=capacity, model=model, place= place)
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
                veh_track = TrackVehicle.objects.create(latitude=None, longitude=None,this_vehicle= vehicle )
                veh_track.save()
                veh_loc = LocationVehicle.objects.create(destination=None,start_place=place,middle_place=None,vehicle=vehicle)
                veh_loc.save()

            except IntegrityError as e:
                return HttpResponseRedirect( '/accounts/add_vehicle' )
        messages.info( request, 'You have added the vehicle successfully!' )
        # return HttpResponseRedirect( '/accounts/add_vehicle' )
        return redirect( add_vehicle_view)
    else:
        add_veh = AddVehicleForm()
    #messages.info( request, 'You have added the vehicle successfully!' )
    return  render(request, 'AddVehicleFormSheet.html', {'add_veh': add_veh})

@login_required
@group_required('Client')
def borrow_vehicle_view(request):
    borr_veh = None
    if request.method == 'POST':
        borr_veh = BorrowVehicleForm(request.POST)
        if borr_veh.is_valid():
            journey_date = borr_veh.cleaned_data['journey_date']
            capacity = borr_veh.cleaned_data['capacity']
            current_place = borr_veh.cleaned_data['current_place']
            destination_place = borr_veh.cleaned_data['destination_place']
            request.session['capacity'] = float(capacity)
            request.session['journey_date'] = str(journey_date)
            request.session['current_place'] = str(current_place)
            request.session['destination_place'] = str(destination_place)
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

@login_required
@group_required('Client')
def borrow_vehicle_list_view(request):
    _capacity = request.session.get('capacity')
    _journey_date = request.session.get('journey_date')
    borrow_vehicle_list = Vehicle.objects.filter( capacity__gte= _capacity ).exclude(journey_date__gte=_journey_date).exclude(client_id__isnull=False).order_by('capacity')
    page = request.GET.get('page', 1)
    #borrow_vehicle = None
    paginator = Paginator(borrow_vehicle_list,3)
    try:
        borrow_vehicle = paginator.page(page)
    except PageNotAnInteger:
        borrow_vehicle = paginator.page(1)
    except EmptyPage:
        borrow_vehicle = paginator.page(paginator.num_pages)
    print(borrow_vehicle_list)
    return render( request, 'BorrowVehicleListSheet.html', {'borrow_vehicle': borrow_vehicle} )

@login_required
@group_required('Client')
def borrow_vehicle_details_view(request, pk):
    prices=0
    try:
        vehicle = Vehicle.objects.get( pk=pk )
        # try:
        #     from .choices import price
        #     cur = str(vehicle.place)
        #     print(cur)
        #
        #     pick = str(request.session['current_place'])
        #     print(pick)
        #     des = str(request.session['destination_place'])
        #     print(des)
        #     prices = price[cur][pick]+price[pick][des]
        # except:
        from geopy.geocoders import Nominatim
        from geopy.distance import geodesic
        geolocator = Nominatim(timeout=40)
        cur = str( vehicle.place )
        des = str( request.session['destination_place'] )
        pick = str( request.session['current_place'] )
        location1 = geolocator.geocode( str(request.session['current_place'])+" bd" )
        location2 = geolocator.geocode( str(vehicle.place)+" bd")
        location3 = geolocator.geocode( str(request.session['destination_place'])+" bd")
        pos1 = (location1.latitude, location1.longitude)
        pos2 = (location2.latitude, location2.longitude)
        pos3 = (location3.latitude, location3.longitude)
        print(pos1,pos2,pos3)
        prices = geodesic( pos1, pos2 ).km+geodesic( pos1, pos3).km

        if datetime.datetime.now().month == 5 or datetime.datetime.now().month== 6:
            if vehicle.capacity >10:
                prices = prices*30*(float(vehicle.capacity)/10.0)
            else:
                prices = prices*30

        else:
            if vehicle.capacity >10:
                prices = prices*33*(float(vehicle.capacity)/10.0)
            else:
                prices = prices*34
        print(prices,type(prices))

    except Vehicle.DoesNotExist:
        raise Http404( "Book does not exist" )
    try:
        if request.method == 'POST' and request.POST['book'] == 'Confirm':
            veh = Vehicle.objects.get( pk=pk )
            if not veh.client:
                veh.client = request.user
                veh.place = request.session['destination_place']
                veh.save()
                veh_loc = LocationVehicle.objects.get( vehicle=vehicle )
                veh_loc.destination = des
                veh_loc.middle_place = pick
                veh_loc.start_place = cur
                veh_loc.save()
                message2 = "You have booked vehicle with license number: "+str(veh.license_no)+"Price: "+ str(prices)+'''
                To contact with owner:
                Owner Name:'''+ str(veh.user.username)+'''
                Email'''+str(veh.user.email)+'''
                phone'''+str(veh.user.address.phone_number)
                message1 = "Your Vehicle with license number: "+str(veh.license_no)+" has been booked by"+'''
                '''+ " Username: "+str(request.user.username)+'''
                 Email:'''+str(request.user.email)+'''
                 Phone: '''+str(request.user.address.phone_number)+'''
                Pay price to client RS: '''+str(prices)

                send_mail(
                    'Vehicle Booking Successful',
                    message2,
                    'mahirmahbub7@gmail.com',
                    [str(veh.user.email)],
                    fail_silently=False,
                )
                send_mail(
                    'Your Vehicle has been Booked',
                    message1,
                    'mahirmahbub7@gmail.com',
                    [str( request.user.email )],
                    fail_silently=False,
                )
                #return HttpResponse("Booked")
                messages.info( request, 'You have booked the vehicle successfully!' )
                return redirect(borrow_vehicle_list_view)
            else:
                # return HttpResponse( 'Can not Book.Already Booked')
                messages.info( request, 'Can not Book.Already Booked' )
                return redirect(borrow_vehicle_list_view)
    except MultiValueDictKeyError:
        raise Http404( "Internal Error" )
        #HttpResponse("Internal Error")

    # book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'BorrowVehicleDetails.html',
        context={'vehicle': vehicle,'prices':prices, 'des':des, 'cur' :cur, "pick":pick }
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

            pk = user.id
            #user = authenticate( username=driver_code, password=passwd_veh )
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login( request, user)
            #raise ValidationError( "username password didn't match" )
            # except:
            #
            #     messages.add_message( request,level=True, message="Wrong username or password" )
            #     #messages.ERROR=True
            #     #driv_log_in.add_error(, "Wrong username oe password" )
            #     return HttpResponseRedirect(request.path_info)
        else:
            messages.add_message( request, level=True, message="Wrong username or password" )
            driv_log_in.add_error( "driver_code", "Wrong username oe password" )
        return HttpResponseRedirect( '/accounts/vehicle_pos/')
    else:
        messages.add_message( request, level=True, message="Wrong username or password" )
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

@login_required
@group_required('Owner')
def added_vehicle_list_view(request):
    user = request.user
    added_vehicle_list = Vehicle.objects.filter( user= user )
    page = request.GET.get('page', 1)
    #borrow_vehicle = None
    paginator = Paginator(added_vehicle_list,4)
    try:
        added_vehicle = paginator.page(page)
    except PageNotAnInteger:
        added_vehicle = paginator.page(1)
    except EmptyPage:
        added_vehicle = paginator.page(paginator.num_pages)
    return render( request, 'AddVehiceListSheet.html', {'added_vehicle': added_vehicle} )

@login_required
@group_required('Owner')
def added_vehicle_details_view(request, pk):
    request.session['pk'] = pk
    try:
        vehicle = Vehicle.objects.get( pk=pk )
        print("Found")
        print(request.POST)
    except Vehicle.DoesNotExist:
        raise Http404( "Book does not exist" )
    try:
        if request.method == 'POST' and request.POST['delete'] == 'Delete':
            veh = Vehicle.objects.get( pk=pk )
            if veh.client_id ==None:
                print("Not Booked")
                veh.delete()
                messages.info(request,"Vehicle has been deleted")
                return redirect(added_vehicle_list_view)
            else:
                messages.info(request,"Can not delete. Already Booked")

                print("Done")
                return redirect(added_vehicle_details_view)
            # return HttpResponse( 'deleted' )
    except:
        try:
            if request.method == 'POST' and request.POST['track'] == 'Track':
                print("Got")
                try:
                    track_vehicle = TrackVehicle.objects.get(this_vehicle_id= pk)
                    print(track_vehicle.latitude)
                    # return render(
                    #     request,
                    #     'Track_borrowed_vehicle.html',
                    #     context={'track_vehicle': track_vehicle, }
                    # )
                    return render(
                        request,
                        'Vehicle_Position.html',
                        context={'track_vehicle': track_vehicle, })
                        #return HttpResponse("Booked")
                except ObjectDoesNotExist:
                    print("Cannot found")
                    HttpResponse("Cannot found")
            # print("ADADA")
            # except MultiValueDictKeyError:
            #     HttpResponse("Internal Error")

            # book_id=get_object_or_404(Book, pk=pk)
        except MultiValueDictKeyError:
            Http404("Internal Error")

    return render(
        request,
        'AddedVehicleDetails.html',
        context={'vehicle': vehicle, }
    )

@login_required
@group_required('Driver')
def own_location_view(request):
    if request.method == 'POST' and request.is_ajax:
        post_text = request.body.decode('utf-8')
        #print(post_text)
        #post_text = json.load(request.body)

        #print("Raw Data: ",re
        # quest.body.decode('utf-8'))
        # if not post_text is None:
        # #
        # #     print(post_text)
        data = post_text.split('&')
        lat = data[0].split("=")[1]
        lon =  data[1].split("=")[1]
        #time = data[2].split("=")[1]
        print(lat,lon)
        user_ = request.user
        print(user_.id)
        pos = TrackVehicle.objects.get(this_vehicle__driver_code_name=user_)

        pos.latitude = float(lat)
        pos.longitude = float(lon)
        import datetime
        pos.time = str(datetime.datetime.now())
        pos.save()
        # HttpResponse( " Got it" )
    return render(
        request,
        'Vehicle_Own_Position.html',)

@login_required
def get_loc_data(request,pk):
    global lan
    track_vehicle = None
    dicto = {}
    print(pk)
    try:
        print("Yay")
        request.session['pk'] = pk
        # veh = Vehicle.objects.get( pk=pk )
        # if not veh.client:
        #     veh.client = request.user
        #     veh.save()
        # try:
        #     if request.method == "GET":
        #         track_vehicle = TrackVehicle.objects.get(this_vehicle_id= pk)
        #         print(track_vehicle.latitude)
        #         lan = track_vehicle.latitude
        #         print(lan)
        #         lng = track_vehicle.longitude
        #         dicto["lan"] = lan
        #         dicto ["lng"] = lng
        #         #return HttpResponse("Booked")
        #         return JsonResponse( dicto )
        # except ObjectDoesNotExist:
        #     print("Cannot found")
        #     HttpResponse("Cannot found")
    except MultiValueDictKeyError:
        HttpResponse("Internal Error")
    return render(request, 'Vehicle_Position.html', dicto)

def get_data(request):
    dicto={}
    pk=request.session['pk']
    try:

        if request.method == "GET":
            track_vehicle = TrackVehicle.objects.get( this_vehicle_id=pk )
            print( track_vehicle.latitude )
            lan = track_vehicle.latitude
            print( lan )
            lng = track_vehicle.longitude
            dicto["lan"] = lan
            dicto["lng"] = lng
            dicto ["time"] = str(track_vehicle.time)
            # return HttpResponse("Booked")
            return JsonResponse( dicto )
    except ObjectDoesNotExist:
        print( "Cannot found" )
        HttpResponse( "Cannot found" )




#
#
#
#
#
@login_required
@group_required('Client')
def Borrowed_vehicle_list_view(request):
    user = request.user
    borrowed_vehicle_list = Vehicle.objects.filter( client= user )
    page = request.GET.get('page', 1)
    #borrow_vehicle = None
    paginator = Paginator(borrowed_vehicle_list,4)
    try:
        borrowed_vehicle = paginator.page(page)
    except PageNotAnInteger:
        borrowed_vehicle = paginator.page(1)
    except EmptyPage:
        borrowed_vehicle = paginator.page(paginator.num_pages)
    return render( request, 'ClientBorrowedVehicleListSheet.html', {'borrowed_vehicle': borrowed_vehicle} )

@login_required
@group_required('Client')
def Borrowed_vehicle_details_view(request, pk):
    request.session['pk'] = pk
    try:
        vehicle = Vehicle.objects.get( pk=pk )
        veh_loc = LocationVehicle.objects.get(vehicle=vehicle)

    except Vehicle.DoesNotExist:
        raise Http404( "Book does not exist" )
    try:
        # if request.method == 'POST' and request.POST['delete'] == 'Delete':
        #     veh = Vehicle.objects.get( pk=pk )
        #     veh.delete()
        #     return HttpResponse( 'deleted' )
        if request.method == 'POST' and request.POST['track'] == 'Track':
            print("Got")
            try:
                track_vehicle = TrackVehicle.objects.get(this_vehicle_id= pk)
                print(track_vehicle.latitude)
                return render(
                    request,
                    'Vehicle_Position.html',
                    context={'track_vehicle': track_vehicle, }
                )
                #return HttpResponse("Booked")
            except ObjectDoesNotExist:

                print("Cannot found")
                #HttpResponse("Cannot found")
    except MultiValueDictKeyError:
        HttpResponse("Internal Error")

    # book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'ClientBorrowedVehicleDetails.html',
        context={'vehicle': vehicle, "loc_veh":veh_loc}
    )


def contact_us(request):

    return render( request, 'Contact.html' )

def credit(request):
    return render( request, 'Credit.html' )
@login_required
def MyProfileView(request):
    user = request.user
    return render(
        request,
        'MyProfile.html',
        context={'user' : user}
    )
