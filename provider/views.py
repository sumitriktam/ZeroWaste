from django.shortcuts import render

def homePage(request):
    return render(request, "frontend/provider/homePage.html")
