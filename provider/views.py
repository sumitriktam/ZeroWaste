from django.shortcuts import render, redirect
from admin_mod.models import User
from .models import post, toysDes, groceryDes, clothDes, foodDes, otherDes
from django.contrib import messages
from datetime import datetime

def homePage(request):
    uid = request.session['user_id']
    try:
        user = User.objects.get(id=uid)
    except:
        messages.error(request, 'You need to login first.')
        return redirect('/login')
    matching_posts = post.objects.filter(user_id=1).order_by('-created_at')
    context = {'uname': user.username, 'email': user.email, 'location':user.location, 'posts':matching_posts}
    return render(request, "provider/dashboard.html", context)

def newPost(request):
    uid = request.session['user_id']
    try:
        user = User.objects.get(id=uid)
    except:
        messages.error(request, 'You need to login first.')
        return redirect('/login')
    context = {}

    if request.method == 'POST':
        data = request.POST
        category = data.get('category')

        #description storing for categories
        if category == 'toys':
            obj = toysDes(age_group=data.get('age-group'), condition=data.get('cond'), desc=data.get('desc'))
 
        if category == 'groceries':
            expiry_date = data.get('expiry-date')
            expiry_time = data.get('expiry-time')
            ex_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            ex_time = datetime.strptime(expiry_time, "%H:%M").time() 
            obj = groceryDes(expiry_date=ex_date, expiry_time=ex_time, desc=data.get('desc'))

        if category == 'clothes':
            obj = clothDes(size=data.get('size'), desc=data.get('desc'), condition=data.get('cond'), gender=data.get('gender'))

        if category == 'food':
            expiry_date = data.get('expiry-date')
            expiry_time = data.get('expiry-time')
            ex_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            ex_time = datetime.strptime(expiry_time, "%H:%M").time() 
            obj = foodDes(expiry_date=ex_date, expiry_time=ex_time, desc=data.get('desc'))

        if category == 'others':
            obj = otherDes(desc=data.get('desc'))

        
        #saving description
        obj.save()

        post_here = post(
            user_id = uid,
            photo = request.FILES.get('photo'),
            category = category,
            drop_pickup = data.get('drop_pickup'),
            description_id = obj.id,
            name = data.get('name'),
            location = data.get('location'),
            will_expire = data.get('will_expire'),
            quantity = data.get('quantity'),
        )
        #saving post
        post_here.save()
        messages.success(request, 'Post succesfully added.')
        return redirect('/provider/home')

    return render(request, "provider/form_newpost.html", context)
    
