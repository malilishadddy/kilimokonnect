from django.urls import path
from . import  views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contactus/',views.contact),
    path('retailers/',views.retailers)

]