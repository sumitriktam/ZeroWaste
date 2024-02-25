from django.shortcuts import render

def index(request):
    context = {}
    #logic here
    return render(request, "admin/home.html", context)

def login(request):
    return render(request, "admin/login.html")

def register(request):
    return render(request, "admin/register.html")