from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utility import get_user_identity
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth.models import User
import requests
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    return render(request, 'profile.html', {'user': user})

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Create the new user object
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Log the user in and redirect to the home page
        authenticated_user = authenticate(request, username=username, password=password)
        login(request, authenticated_user)
        
        user_identity = get_user_identity(request.user)
        return redirect(user_identity)


    return render(request, 'register.html', {})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            user_identity = get_user_identity(user)
            return redirect(user_identity)
            ...
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Invalid Details"))
            return redirect('login')
            ...
    return render(request, 'login.html', {'request': request})

def logout_user(request):
    logout(request)
    return redirect('index')

def server_info(request):
    server_geodata = requests.get('https://ipwhois.app/json/').json()
    settings_dump = settings.__dict__
    return HttpResponse("{}{}".format(server_geodata, settings_dump))