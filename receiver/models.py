from django.db import models
from provider.models import User,post
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    ordered_post=models.ForeignKey(post,related_name='orders',on_delete=models.CASCADE)
    date_time= models.DateTimeField(default=timezone.localtime)
    receiver_user=models.ForeignKey(User,on_delete=models.CASCADE)
    STATUS_OPTIONS=(
        ('accept','Accept'),
        ('reject','Reject'), 
        ('pending','Pending'),
        ('delivered','Delivered')
    )
    status=models.CharField(max_length=10,choices=STATUS_OPTIONS,default='pending')
    receiver_location=models.CharField(max_length=30)
    quantity=models.IntegerField()

