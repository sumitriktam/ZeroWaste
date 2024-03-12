from admin_mod.models import User
from provider.models import post
from django.shortcuts import get_object_or_404

def auth(request):
    try: 
        uid = request.session['user_id']
        user = get_object_or_404(User, pk=uid)
        if user.role != 'provider':
            return False 
        return user
    except:
        return False
    
def post_auth(request, post_id, u):
    try:
        p = post.objects.get(id=post_id)
    except:
        return False
    # print("this ran $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    if p.user== u:
        return p 
    return False

