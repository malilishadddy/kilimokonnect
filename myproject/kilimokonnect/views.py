from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,'kilimokonnect/index.html')
    # return render(request,'kilimokonnect/frame.html')
def about(request):
    return  render(request, 'kilimokonnect/about.html')
def retailers(request):
    return  render(request, 'kilimokonnect/retailersmain.html')
def contact(request):
    return  render(request, 'kilimokonnect/retailersorders.html')
