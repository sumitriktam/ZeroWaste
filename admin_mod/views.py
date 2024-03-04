import json
from django.shortcuts import render, redirect
from django import forms
from .models import User, Admin, Resetpass
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .custom_auth import  CustomBackend
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
import uuid
from .mail_helper import send_forget_password_mail

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

    # Here, counting the users for each status
    accepted_count = accepted_users.count()
    pending_count = pending_users.count()
    rejected_count = rejected_users.count()

    context = {
        'accepted_users': accepted_users,
        'pending_users': pending_users,
        'rejected_users': rejected_users,
        'accepted_count': accepted_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
    }
    return render(request, "admin/adminPanel.html", context)

from django.db.models import Count

def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'accepted'
    user.save(update_fields=['status'])

    accepted_users = User.objects.filter(status='accepted')
    pending_users = User.objects.filter(status='pending')
    rejected_users = User.objects.filter(status='rejected')

    accepted_count = accepted_users.count()
    pending_count = pending_users.count()
    rejected_count = rejected_users.count()

    data = {
        'accepted_users': list(accepted_users.values()),
        'pending_users': list(pending_users.values()),
        'rejected_users': list(rejected_users.values()),
        'accepted_count': accepted_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
    }
    return JsonResponse(data)

def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'rejected'
    user.save(update_fields=['status'])

    accepted_users = User.objects.filter(status='accepted')
    pending_users = User.objects.filter(status='pending')
    rejected_users = User.objects.filter(status='rejected')

    accepted_count = accepted_users.count()
    pending_count = pending_users.count()
    rejected_count = rejected_users.count()

    data = {
        'accepted_users': list(accepted_users.values()),
        'pending_users': list(pending_users.values()),
        'rejected_users': list(rejected_users.values()),
        'accepted_count': accepted_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
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
                return  redirect("receiver/home")
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

def ChangePassword(request , token):
    context = {}
    try:
        profile_obj = Resetpass.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/') 
        
        
    except Exception as e:
        print(e)
    return render(request , 'change-password.html' , context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Resetpass.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')