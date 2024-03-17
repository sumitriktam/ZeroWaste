from datetime import datetime, timedelta
from django.utils import timezone
from .models import post, FeedbackTab

base_score = 100
multipliers = {'clothes': 1, 'toys': 1.4, 'groceries': 6, 'food': 2.5, 'others': 1}

def calculate_feedback_score(rating):
    return (rating / 5) * 100

def calculate_zerowaste_score(category):
    return base_score * multipliers.get(category, 1)

def calculate_streak_multiplier(user_id):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    streak_multiplier = 1
    current_date = today
    while streak_multiplier < 2 and post.objects.filter(user_id=user_id, created_at__date=current_date).exists():
        streak_multiplier += 0.1
        current_date -= timedelta(days=1)
    return streak_multiplier

def calculate_total_score(request, post_id):
    quantity = int(post.objects.get(id=post_id).quantity)
    category = post.objects.get(id=post_id).category
    feedback_rating = FeedbackTab.objects.filter(post_id=post_id).first().rating
    feedback_score = calculate_feedback_score(feedback_rating)
    zerowaste_score = calculate_zerowaste_score(category)
    user_id = request.session['user_id']
    streak_multiplier = calculate_streak_multiplier(user_id)
    total_score = ((zerowaste_score * quantity) + feedback_score) * streak_multiplier
    return total_score
