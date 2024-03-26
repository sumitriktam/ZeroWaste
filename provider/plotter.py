from admin_mod.models import User
from .models import scoreHistory 
from django.shortcuts import get_object_or_404

def returnhistory(user_id):
    score = []
    date = []
    user = User.objects.get(id = user_id)
    history = scoreHistory.objects.filter(user=user)
    for h in history:
        score.append(h.score)
        date_str = h.date_time.strftime("%Y-%m-%d")
        date.append(date_str)
    return (score, date)
