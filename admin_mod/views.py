import json
from django.shortcuts import render, redirect
from django import forms
from .models import User, Admin, Resetpass, EmailVerification, adminReg
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .custom_auth import  CustomBackend, auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
import uuid
from .mail_helper import send_forget_password_mail, send_user_confirmation_email, send_admin_reg_email
from django.utils import timezone
from datetime import timedelta, datetime
from provider.models import post, toysDes, groceryDes, clothDes, foodDes, otherDes
from receiver.models import Order
from .admin_auth import CustomBackend1, auth1


def index(request):
    #only get users who are providers and whose status is accepted
    #other condition is get users whose zerowaste score is grater than zero because by default we're assigning everyone a score of zero
    users = User.objects.filter(status="accepted", role="provider", zerowaste_score__gt=0).order_by('-zerowaste_score')[:9]
    context = {
        'users': users
    }
    return render(request, "admin/home.html", context)

def showUsers(request):
    accepted_users = User.objects.filter(status='accepted')
    pending_users = User.objects.filter(status='pending')
    rejected_users = User.objects.filter(status='rejected')

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
    return render(request, "admin/showUsers.html", context)




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
            if isinstance(user, User):
                request.session['user_id'] = user.id
                if user.is_verified == 0:
                    return redirect('email-verification-pending/')
                elif user.status == 'pending':
                    return redirect("/wait")
                elif user.status == 'rejected':
                    return redirect("/application-rejected")
                elif user.role == 'provider':
                    return redirect("provider/home")
                elif user.role == 'receiver':
                    request.session['role'] = 'receiver'
                    return redirect("/receiver/home")
                else:
                    return redirect('/register')
            elif isinstance(user, Admin):
                request.session['admin_id'] = user.id
                if user.status == 'active':
                    request.session['role'] = 'admin'
                    return redirect("/adminPanel")
                else:
                    messages.error(request, 'Admin status inactive.')
                    return redirect('/login')
        else:
            admin_backend = CustomBackend1()
            user = admin_backend.authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                request.session['super_admin_id'] = user.id
                request.session['role'] = 'superadmin'
                return redirect("/adminPanel")
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
        fields = ['email', 'username', 'password', 'location', 'role', 'is_verified']


# views.py
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_user_confirmation_email(user)
            return redirect('/email-verification-pending/')
    else:
        form = UserForm()
    return render(request, 'admin/register.html', {'form': form})


# views.py
def email_verification_pending(request):
    return render(request, 'admin/verification_pending.html')

def email_verified(request):
    return render(request, 'admin/email_confirmed.html')


def confirm_account(request, token):
    try:
        verification = get_object_or_404(EmailVerification, token=token)
        user = verification.user
        print(user)
        if user.is_verified:
            messages.success(request, 'Email already verified.')
            return redirect('/login')
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        verification.delete()
        return redirect('/email-verified/')
    except:
        error_message = 'Invalid URL.'
        return render(request, 'admin/failed_verification.html', {'error_message': error_message})
    

def failed_to_verify(request):
    return render(request, 'admin/failed_verification.html')




def waitingPage(request):
    return render(request, "admin/waitingPage.html")
    

def change_password(request, token):
    context = {}
    try:
        profile_obj = Resetpass.objects.filter(forget_password_token=token).first()
        # print(token)
        # print(Resetpass.objects.get(forget_password_token=token))
        if profile_obj is None:
            return redirect('/invalid-token/')

        # Check if the token is older than 30 minutes
        if profile_obj.created_at < timezone.now() - timedelta(minutes=30):
            messages.success(request, 'Token has expired.')
            profile_obj.delete()
            return redirect('/forget-password/')
        
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            # print(user_id)

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/forget-password/')

            if new_password != confirm_password:
                messages.success(request, 'Passwords do not match.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            # hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user_obj.password = new_password
            user_obj.save()
            profile_obj.delete()  # Delete the Resetpass entry
            return redirect('/login')

    except Exception as e:
        print(e)
        messages.success(request, 'link expired.')
    return render(request, 'admin/change_password.html', context)


def forget_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')

            if email == '':
                messages.success(request, 'No email provided.')
                return redirect('/forget-password/')
            if not User.objects.filter(email=email).exists():
                messages.success(request, 'No user found with this email.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(email=email)
            resetpass_obj, created = Resetpass.objects.get_or_create(user=user_obj)
            if not created:
                if resetpass_obj.created_at < timezone.now() - timedelta(minutes=30):
                    resetpass_obj.forget_password_token = str(uuid.uuid4())
                    resetpass_obj.created_at = timezone.now()
                    resetpass_obj.save()
                    send_forget_password_mail(user_obj.email, resetpass_obj.forget_password_token)
                    messages.success(request, 'An email is sent.')
                    return redirect('/forget-password/')
                else:
                    messages.success(request, 'A verification email was already sent. Please check your inbox.')
                    return redirect('/forget-password/')
            else:
                resetpass_obj.forget_password_token = str(uuid.uuid4())
                resetpass_obj.created_at = timezone.now()
                resetpass_obj.save()
                send_forget_password_mail(user_obj.email, resetpass_obj.forget_password_token)
                messages.success(request, 'An email is sent.')
                return redirect('/forget-password/')
    
    except Exception as e:
        print(e)
    return render(request, 'admin/forgot_password.html')

def resend_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email == '':
            messages.success(request, 'No email provided.')
            return redirect('/forget-password/')
        # print("email is : ", email)
        try:
            user_obj = User.objects.get(email=email)
            resetpass_obj = Resetpass.objects.get(user=user_obj)
            if resetpass_obj.created_at < timezone.now() - timedelta(minutes=30):
                resetpass_obj.forget_password_token = str(uuid.uuid4())
                resetpass_obj.created_at = timezone.now()
                resetpass_obj.save()
                send_forget_password_mail(user_obj.email, resetpass_obj.forget_password_token)
                messages.success(request, 'An email is sent.')
                return redirect('/forget-password/')
            else:
                # print("it is in else block and email is sent")
                send_forget_password_mail(user_obj.email, resetpass_obj.forget_password_token)
                messages.success(request, 'An email is sent.')
                return redirect('/forget-password/')
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to resend email. Please try again later.')
    return redirect('/forget-password/')

def invalid_token(request):
    return render(request, 'admin/invalid_token.html')



def application_rejected(request):
    return render(request, 'admin/rejecteduser.html')

def adminPanel(request):
    user = auth(request)
    superadmin = auth1(request)
    if not user and not superadmin:
        messages.error(request, 'You need to login first.')
        return redirect("/login")
    return render(request, 'admin/showUsers.html')

def showOrders(request):
    return render(request, 'admin/showOrders.html')

def showPosts(request):
    posts_with_descriptions = []
    posts = post.objects.all().order_by('-created_at')
    for single_post in posts:
        toys_desc = None
        grocery_desc = None
        cloth_desc = None
        food_desc = None
        other_desc = None
        if single_post.category == 'toys':
            toys_desc = toysDes.objects.filter(id=single_post.description_id).first()
        elif single_post.category == 'groceries':
            grocery_desc = groceryDes.objects.filter(id=single_post.description_id).first()
            print(grocery_desc)

        elif single_post.category == 'clothes':
            cloth_desc = clothDes.objects.filter(id=single_post.description_id).first()
        elif single_post.category == 'food':
            food_desc = foodDes.objects.filter(id=single_post.description_id).first()
        elif single_post.category == 'others':
            other_desc = otherDes.objects.filter(id=single_post.description_id).first()
        posts_with_descriptions.append({
            'post': single_post,
            'toys_desc': toys_desc,
            'grocery_desc': grocery_desc,
            'cloth_desc': cloth_desc,
            'food_desc': food_desc,
            'other_desc': other_desc,
        })
    context = {
        'posts_with_descriptions': posts_with_descriptions,
    }
    return render(request, 'admin/showPosts.html', context)

def showAdmins(request):
    return render(request, 'admin/showAdmins.html')


def save_post_changes(request):
    # print("It reached function")
    def convert_time_to_duration(time_str):
        time_mapping = {
            "midnight": "00:00:00:000000",
            "noon": "12:00:00:000000",
            "a.m": "00:00:00",
            "p.m": "12:00:00"
        }

        if time_str.lower() in time_mapping:
            return time_mapping[time_str.lower()]

        parts = time_str.strip().lower().split()
        if len(parts) != 2:
            raise ValueError("Invalid time format")

        hour, minute = parts[0].split(':')
        if parts[1] == 'a.m':
            if hour == '12':
                hour = '00'
        elif parts[1] == 'p.m':
            if hour != '12':
                hour = str(int(hour) + 12)
        else:
            raise ValueError("Invalid time format")

        return f"{hour.zfill(2)}:{minute.zfill(2)}:00:000000"
    if request.method == 'POST':
        post_id = request.POST.get('editPostId')
        print("post Id is : ", post_id)
        post_obj = post.objects.get(pk=post_id)
        post_obj.name = request.POST.get('editName')
        post_obj.category = request.POST.get('editCategory')
        post_obj.drop_pickup = request.POST.get('editdropPickup')
        post_obj.location = request.POST.get('editLocation')
        post_obj.will_expire = request.POST.get('editwillExpire')
        post_obj.status = request.POST.get('editStatus')

        if post_obj.category == 'toys':
            toys_desc, created = toysDes.objects.get_or_create(id=post_obj.description_id)
            toys_desc.desc = request.POST.get('editToysDesc', '')
            toys_desc.age_group = request.POST.get('editAgeGroup', 0)
            toys_desc.condition = request.POST.get('editConditionToys', '')
            toys_desc.save()

        elif post_obj.category == 'groceries':
            grocery_desc, created = groceryDes.objects.get_or_create(id=post_obj.description_id)
            grocery_desc.desc = request.POST.get('editGroceryDesc', '')
            grocery_desc.expiry_date = datetime.strptime(request.POST.get('editExpiryDate', ''), "%B %d, %Y").strftime("%Y-%m-%d")
            ins_time = request.POST.get('editExpiryTime', '')
            data_time = convert_time_to_duration(ins_time)
            print(data_time)
            grocery_desc.expiry_time = data_time
            grocery_desc.save()

        elif post_obj.category == 'clothes':
            cloth_desc, created = clothDes.objects.get_or_create(id=post_obj.description_id)
            cloth_desc.desc = request.POST.get('editClothDesc', '')
            cloth_desc.gender = request.POST.get('editGender', '')
            cloth_desc.condition = request.POST.get('editConditionCloth', '')
            cloth_desc.size = request.POST.get('editSize', '')
            cloth_desc.save()

        elif post_obj.category == 'food':
            food_desc, created = foodDes.objects.get_or_create(id=post_obj.description_id)
            food_desc.desc = request.POST.get('editFoodDesc', '')
            food_desc.expiry_date = request.POST.get('editExpiryDateFood', '')
            food_desc.expiry_time = request.POST.get('editExpiryTimeFood', '')
            food_desc.save()

        elif post_obj.category == 'others':
            other_desc, created = otherDes.objects.get_or_create(id=post_obj.description_id)
            other_desc.desc = request.POST.get('editOtherDesc', '')
            other_desc.save()

        post_obj.save()
        return redirect('/posts/')
    return redirect('/posts/')

def delete_post(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        post_del = post.objects.get(id=post_id)
        post_del.delete()
        return redirect('/posts/')

def showAdmins(request):
    accepted_admins = Admin.objects.filter(status='active')
    rejected_admins = Admin.objects.filter(status='inactive')

    accepted_count = accepted_admins.count()
    rejected_count = rejected_admins.count()

    context = {
        'active_admins': accepted_admins,
        'inactive_admins': rejected_admins,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
    }
    return render(request, "admin/showAdmins.html", context)


def approve_admin(request, admin_id):
    admin = get_object_or_404(Admin, id=admin_id)
    admin.status = 'active'
    admin.save(update_fields=['status'])

    accepted_admins = Admin.objects.filter(status='active')
    rejected_admins = Admin.objects.filter(status='inactive')

    accepted_count = accepted_admins.count()
    rejected_count = rejected_admins.count()

    data = {
        'active_admins': list(accepted_admins.values()),
        'inactive_admins': list(rejected_admins.values()),
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
    }
    return JsonResponse(data)

def reject_admin(request, admin_id):
    admin = get_object_or_404(Admin, id=admin_id)
    admin.status = 'inactive'
    admin.save(update_fields=['status'])

    accepted_admins = Admin.objects.filter(status='active')
    rejected_admins = Admin.objects.filter(status='inactive')

    accepted_count = accepted_admins.count()
    rejected_count = rejected_admins.count()

    data = {
        'active_admins': list(accepted_admins.values()),
        'inactive_admins': list(rejected_admins.values()),
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
    }
    return JsonResponse(data)


def send_regEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        if email == '':
            messages.success(request, 'No email provided.')
            return redirect('/forget-password/')
        send_admin_reg_email(email)
    return redirect('/admins/')

def reg_admin(request, token):
    try:
        verification = get_object_or_404(adminReg, token=token)
        user = verification.email
        print(user)
        if user is not None:
            return render(request, 'admin/adminReg.html')
        else:
            error_message = 'Invalid URL.'
            return render(request, 'admin/invalid_token.html', {'error_message': error_message})

    except:
        error_message = 'Invalid URL.'
        return render(request, 'admin/invalid_token.html', {'error_message': error_message})
    

def adminRegister(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        location = request.POST.get('location')

        # Save data to the Admin model
        admin = Admin(email=email, username=username, password=password, location=location)
        admin.save()
        return redirect('registration_success')

    return render(request, 'admin/adminReg.html')


def registration_success_view(request):
    return render(request, 'admin/registration_success.html')

def showOrders(request):
    orders=Order.objects.all()
   #seperate all kinds of orders made by this user
    accepted=[]
    pending=[]
    rejected=[]
    delivered=[] #receiver have a button wether the order is delivered or not when he clicks on that the status will be updated to delivered(not yet implemented)  
    for order in orders:
        order_details={}
        order_details['status']=order.status
        order_details['order_id']=order.id
        order_details['date']=order.date_time.strftime('%d-%m-%Y')
        order_details['time']=order.date_time.strftime('%H:%M')
        order_details['quantity']=order.quantity
        order_details['receiver_user'] = order.receiver_user.username

        if(order.status=='accepted'):
            accepted.append(order_details)
        elif(order.status=='pending'):
            pending.append(order_details)
        elif(order.status=='rejected'):
            rejected.append(order_details)
        else:
            delivered.append(order_details)
        
        #take image,item_name,user_post location from user_post table
        user_post=post.objects.get(id=order.ordered_post_id)
        order_details['image']=user_post.photo.url
        order_details['item_name']=user_post.name
        order_details['location']=user_post.location
        order_details['post_user'] = user_post.user.username
        #take location from user table
        
    all_orders={
        'accepted':accepted,
        'pending':pending,
        'rejected':rejected,
        'delivered':delivered,
        }
           

    return render(request, 'admin/showOrders.html' , {'orders':all_orders})

def edit_order(request):
    if request.method == 'POST' :
        # Get the form data
        status = request.POST['status']
        order_id = request.POST['order_id']
        date = request.POST['date']
        time = request.POST['time']
        quantity = request.POST['quantity']
        image = request.POST['image']
        item_name = request.POST['item_name']
        location = request.POST['location']
        receiver_user = request.POST['receiver_user']
        post_user = request.POST['post_user']

        # Get the order object from the database
        order = Order.objects.get(pk=order_id)
        user_post=post.objects.get(id=order.ordered_post_id)

        
        # Update the order with the new data
        order.status = status
        order.receiver_user.username = receiver_user
        order.quantity = quantity
        # user_post.photo.url = image
        user_post.user.username = post_user
        user_post.name = item_name
        user_post.location = location
        order.save()
        user_post.save()
        
        
        return JsonResponse({'message': 'Order updated successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request!'}, status=400)
    

def delete_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.delete()
        return JsonResponse({'message': 'Order deleted successfully!'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order does not exist'}, status=404)
    
def logout(request):
    request.session.flush()
    return redirect('/')