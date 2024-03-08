import json
from django.shortcuts import render, redirect
from django import forms
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .custom_auth import  CustomBackend
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def index(request):
    #only get users who ate providers and whose status is accepted
    #other condition is get users whose zerowaste score is grater than zero because by default we're assigning everyone a score of zero
    users = User.objects.filter(status="accepted", role="provider", zerowaste_score__gt=0).order_by('-zerowaste_score')[:9]
    context = {
        'users': users
    }
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
    return render(request, "admin/adminPanel.html", context)

def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'accepted'
    user.save(update_fields=['status'])

    accepted_users = User.objects.filter(status='accepted')
    pending_users = User.objects.filter(status='pending')
    rejected_users = User.objects.filter(status='rejected')

    data = {
        'accepted_users': list(accepted_users.values()),
        'pending_users': list(pending_users.values()),
        'rejected_users': list(rejected_users.values()),
    }
    return JsonResponse(data)

def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'rejected'
    user.save(update_fields=['status'])

    accepted_users = User.objects.filter(status='accepted')
    pending_users = User.objects.filter(status='pending')
    rejected_users = User.objects.filter(status='rejected')

    data = {
        'accepted_users': list(accepted_users.values()),
        'pending_users': list(pending_users.values()),
        'rejected_users': list(rejected_users.values()),
    }
    return JsonResponse(data)

def check_user_existence(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)
        else:
            return JsonResponse({'success': 'User does not exist'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        custom_backend = CustomBackend()
        user = custom_backend.authenticate(request, email=email, password=password)
        # regUser = custom_backend.authenticate(request, email=email)
        
        if user is not None:
            request.session['user_id'] = user.id
            if user.status == 'pending':
                return  redirect("/wait")
            elif user.role=='admin':
                return  redirect("/adminPanel")
            elif user.role=='provider':
                return  redirect("provider/home")
            elif user.role=='receiver':
                return  redirect("receiver")
            else:
                return redirect('/register')
        else:
            request.session['user_id'] = 0    #invalidated user
            messages.error(request, 'Invalid email or password.')
            return redirect('/login')
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
            return redirect('/wait')
        else:
            print(form.errors)
    else:
        print('get request')
        form = UserForm()
    return render(request, 'admin/register.html', {'form': form})

def waitingPage(request):
    return render(request, "admin/waitingPage.html")
