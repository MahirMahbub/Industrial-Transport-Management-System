"""ITMS_Project_Final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Authentication import views
from Authentication.views import address_view, dummy, add_vehicle_view, driver_login, borrow_vehicle_view, \
    borrow_vehicle_list_view, borrow_vehicle_details_view, added_vehicle_list_view, added_vehicle_details_view, \
    own_location_view, get_loc_data, get_data, Borrowed_vehicle_details_view, Borrowed_vehicle_list_view, contact_us, \
    credit, MyProfileView

#borrow_vehicle_view,borrow_vehicle_list_view

urlpatterns = [
   # path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    #path('accounts/logout/', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    path('accounts/', include('allauth.urls')),
    path('accounts/address/',address_view, name = "address_view"),
    path( '', dummy, name = "dummy" ),
    path('accounts/driver_login/',driver_login, name = "driver_login"),
    path('accounts/add_vehicle/', add_vehicle_view, name = "add_vehicle_view"),
    path('accounts/borrow_vehicle/', borrow_vehicle_view, name = "borrow_vehicle_view"),
    path('accounts/borrow_vehicle_list/', borrow_vehicle_list_view, name = "borrow_vehicle_list_view"),
    path('accounts/borrow_vehicle_details/<int:pk>', borrow_vehicle_details_view, name='borrow_vehicle_details_view'),
    path('accounts/added_vehicle_list/', added_vehicle_list_view, name = "added_vehicle_list_view"),
    path('accounts/added_vehicle_details/<int:pk>', added_vehicle_details_view, name='added_vehicle_detail_view'),
    # path( 'chat/', include( 'django_private_chat.urls' ) ),
    path("accounts/vehicle_pos/", own_location_view, name = "own_location_view"),
    path("accounts/get_loc_data/<int:pk>",get_loc_data, name = "get_loc_data"),
    path("accounts/get_data/",get_data, name = "get_data"),
    path( 'accounts/borrowed_vehicle_list/', Borrowed_vehicle_list_view, name="Borrowed_vehicle_list_view" ),
    path( 'accounts/borrowed_vehicle_details/<int:pk>', Borrowed_vehicle_details_view, name='Borrowed_vehicle_detail_view' ),
    path ('accounts/contact_us', contact_us, name  = "contact_us"),
    path ('accounts/credit', credit, name  = "credit"),
    path('accounts/my_profile', MyProfileView, name = "MyProfileView"),
]
