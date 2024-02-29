from django.shortcuts import render, redirect
from admin_mod.models import User
from .models import post
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


