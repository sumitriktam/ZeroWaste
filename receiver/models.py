from django.db import models
from provider.models import User,post
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    ordered_post=models.ForeignKey(post,on_delete=models.CASCADE)
    date_time= models.DateTimeField(default=timezone.now)
    receiver_user=models.ForeignKey(User,on_delete=models.CASCADE)
    STATUS_OPTIONS=(
        ('accept','Accept'),
        ('reject','Reject'), 
        ('pending','Pending'),
    )
    status=models.CharField(max_length=10,choices=STATUS_OPTIONS,default='pending')
    receiver_location=models.CharField(max_length=30)
    quantity=models.IntegerField()

class Feedback(models.Model):
    post_id = models.ForeignKey(post, on_delete=models.CASCADE)  
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    feedback = models.CharField(max_length=500, default="")