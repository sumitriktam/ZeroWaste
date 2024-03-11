from django.shortcuts import render, redirect
from admin_mod.models import User 
from receiver.models import Order
from .models import post, toysDes, groceryDes, clothDes, foodDes, otherDes, FeedbackTab
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404

def homePage(request):
    uid = request.session['user_id']
    try: 
        user = get_object_or_404(User, pk=uid)
    except:
        messages.error(request, 'You need to login first.')
        return redirect('/login')
    matching_posts = post.objects.filter(user=user).order_by('-created_at')

    orders = Order.objects.filter(ordered_post__user=user)  #problem is here
    
    context = {'uname': user.username, 'email': user.email, 'location':user.location, 'posts':matching_posts, 'orders':orders}
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
        messages.success(request, 'Post successfully added.')
    
        # Redirect to the dashboard or any other page with the success message as a parameter in the URL
        return redirect('/provider/home')
        

    return render(request, "provider/form_newpost.html", context)

def requestsViewAll(request):
    return render(request,"provider/requests.html" )

def allPosts(request):
    uid = request.session['user_id']
    try:
        user = User.objects.get(id=uid)
    except:
        messages.error(request, 'You need to login first.')
        return redirect('/login')
    posts_with_descriptions = []
    posts = post.objects.filter(user_id=uid).order_by('-created_at')
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
    return render(request, "provider/all_posts.html", context)

def feedback(request, post_id):
    uid = request.session['user_id']
    try: 
        user = get_object_or_404(User, pk=uid)
    except:
        messages.error(request, 'You need to login first.')
        return redirect('/login')
    feedbacks = FeedbackTab.objects.filter(post_id=post_id)
    return render(request, "provider/feedback.html", context={'feedbacks':feedbacks, "pid":post_id})
    

