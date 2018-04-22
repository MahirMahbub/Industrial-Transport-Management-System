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
    borrow_vehicle_list_view, borrow_vehicle_details_view, added_vehicle_list_view, added_vehicle_details_view

#borrow_vehicle_view,borrow_vehicle_list_view

urlpatterns = [
   # path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    #path('accounts/logout/', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    path('accounts/', include('allauth.urls')),
    path('accounts/address/',address_view, name = "address_view"),
    path( '', dummy ),
    path('accunts/driver_login/',driver_login, name = "driver_login"),
    path('accounts/add_vehicle/', add_vehicle_view, name = "add_vehicle_view"),
    path('accounts/borrow_vehicle/', borrow_vehicle_view, name = "borrow_vehicle_view"),
    path('accounts/borrow_vehicle_list/', borrow_vehicle_list_view, name = "borrow_vehicle_list_view"),
    path('accounts/borrow_vehicle_details/<int:pk>', borrow_vehicle_details_view, name='borrow_vehicle_details_view'),
    path('accounts/added_vehicle_list/', added_vehicle_list_view, name = "added_vehicle_list_view"),
    path('accounts/added_vehicle_details/<int:pk>', added_vehicle_details_view, name='added_vehicle_detail_view'),

]
