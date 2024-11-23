from django.urls import path
from . import  views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contactus/',views.contact),
    path('signup/',views.signup),
    path('login/',views.login),
    path('retailersdash/',views.retailersdashboard),
    path('retailersavailableproduce/',views.retailersavailable),
    path('retailersbookstorage/',views.bookstorage),
    path('retailersanalytics/',views.retailersanalytics),
    path('retailersnotification/',views.retailersnotification),
    path('ownersdashboard/',views.ownersdash),
    path('ownersstoragerequest/',views.storagerequest),
    path('ownersinventory/',views.ownerinventory),
    path('ownersfinancials/',views.ownersfinancials),
    path('ownersnotifications/',views.ownernotification),
    path('retailersorders/',views.retailersorder),




    

]