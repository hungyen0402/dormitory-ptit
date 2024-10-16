from django.shortcuts import *
from django.contrib.auth import authenticate, login as dlogin, logout as dlogout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *



def welcome_page(request):
    rooms = Rooms.objects.all()
    for room in rooms:
        print(room.image1.url)
    context = {"rooms":rooms}
    return render(request, "home.html", context)


def login_page(request):
    context = {}
    return render(request, "login.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password = password)
        if user is not None:
            dlogin(request, user)
            if username == "admin" or username == "admin_user":
                return redirect("admin-welcome-page")
            else:
                return redirect("welcome-page")
        messages.error(request, "Invalid Login Details")
        return redirect("login-page")
    else:
        return redirect("login-page")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username = username, password = password)
        user.save()
        return redirect("login-page")
    context = {}
    return render(request, "signup.html", context)


def view_rooms(request):
    rooms = Rooms.objects.all()
    context = {"rooms":rooms}
    return render(request, "view_rooms.html", context)


def logout_page(request):
    dlogout(request)
    return redirect("/")
