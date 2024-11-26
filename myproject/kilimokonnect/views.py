from django.shortcuts import render, redirect
from .forms import User
from django.http import HttpResponse 

def signup(request):
    if request.method == 'POST':
        form = User(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('success_page')  # Redirect to a success page or login page
    else:
        form = User()
    
    return render(request, 'kilimokonnect/signup.html', {'form': form})


# Create your views here.
def index(request):
    return render(request,'kilimokonnect/index.html')
    # return render(request,'kilimokonnect/frame.html')
def about(request):
    return  render(request, 'kilimokonnect/about.html')
def login(request):
    return  render(request, 'kilimokonnect/login.html')
#def signup(request):
 #   return  render(request, 'kilimokonnect/signup.html')
def contact(request):
    return  render(request, 'kilimokonnect/contactus.html')
def retailersdashboard(request):
    return  render(request, 'kilimokonnect/retailersdash.html')
def retailersavailable(request):
    return  render(request, 'kilimokonnect/retailersavailableprodece.html')
def bookstorage(request):
    return  render(request, 'kilimokonnect/bookstorage.html')
def retailersanalytics(request):
    return  render(request, 'kilimokonnect/retailersanalytics.html')
def retailersnotification(request):
    return  render(request, 'kilimokonnect/retailersnotifications.html')
def ownersdash(request):
    return  render(request, 'kilimokonnect/ownersdashboard.html')
def storagerequest(request):
    return  render(request, 'kilimokonnect/ownersstoragerequest.html')
def ownerinventory(request):
    return  render(request, 'kilimokonnect/ownersiventory.html')
def ownersfinancials(request):
    return  render(request, 'kilimokonnect/ownersfinancials.html')
def ownernotification(request):
    return  render(request, 'kilimokonnect/ownersnotification.html')
def retailersorder(request):
    return  render(request, 'kilimokonnect/retailersorders.html')
