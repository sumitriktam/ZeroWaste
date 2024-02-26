from django.shortcuts import render, redirect
from django import forms
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .custom_auth import  CustomBackend
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def index(request):
    context = {}
    #logic here
    return render(request, "admin/home.html", context)

def adminPanel(request):
    accepted_users = User.objects.filter(status='accepted')  
    pending_users = User.objects.filter(status='pending')
    rejected_users = User.objects.filter(status='rejected')
    
    context = {
        'accepted_users': accepted_users,
        'pending_users': pending_users,
        'rejected_users': rejected_users,
    }
    return render(request, "admin/adminPanel.html")

def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'accepted'
    user.save()
    return JsonResponse({'message': 'User approved successfully'})

def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    print(user)
    user.status = 'rejected'
    user.save()
    return JsonResponse({'message': 'User rejected successfully'})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Instantiate your custom authentication backend
        custom_backend = CustomBackend()
        
        # Use the authenticate method of the custom authentication backend to authenticate the user
        user = custom_backend.authenticate(request, email=email, password=password)
        
        if user is not None:
            # Authentication successful, log the user in
            request.session['user_id'] = user.id
            if user.role=='admin':
                return  redirect("adminPanel")
            elif user.role=='provider':
                return  redirect("providerHome")
            elif user.role=='receiver':
                return  redirect("receiverHome")
            # Redirect to dashboard or profile page
            else:
                # need to add a alert showing the user is not registered, then redirect to register page
                return redirect('register')
        else:
            # Authentication failed
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    else:
        # Render the login page
        return render(request, 'admin/login.html' , {"message":messages.get_messages(request)})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'location', 'role']

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('wait')
        else:
            print(form.errors)
    else:
        print('get request')
        form = UserForm()
    return render(request, 'admin/register.html', {'form': form})

def waitingPage(request):
    return render(request, "admin/waitingPage.html")
