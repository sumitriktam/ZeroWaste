from django.shortcuts import render, redirect
from admin_mod.models import User
from .models import post, toysDes
from django.contrib import messages

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
        if category == 'toys':
            toy = toysDes(age_group=data.get('age-group'), condition=data.get('cond'), desc=data.get('desc'))
            toy.save()
            desc_id = toy.id
        post_here = post(
            user_id = uid,
            photo = request.FILES.get('photo'),
            category = category,
            drop_pickup = data.get('drop_pickup'),
            description_id = desc_id,
            name = data.get('name'),
            location = data.get('location'),
            will_expire = data.get('will_expire'),
            quantity = data.get('quantity'),
        )
        post_here.save()
        messages.success(request, 'Post succesfully added.')
        return redirect('/provider/home')

    return render(request, "provider/newpost.html", context)
    


