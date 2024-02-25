from django.shortcuts import render

def index(request):
    context = {}
    #logic here
    return render(request, "admin/home.html", context)

