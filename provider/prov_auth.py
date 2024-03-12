from admin_mod.models import User 
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