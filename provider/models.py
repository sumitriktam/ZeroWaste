from django.db import models
from admin_mod.models import User 
from django.utils import timezone


# Create your models here.
class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='statics/provider/postpics', blank=True)
    CATEGORY_CHOICES = (
        ('toys', 'Toys'), 
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('others', 'Others'),
        ('groceries', 'Groceries')
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    DROP_PICKUP_CHOICES = (
        ('drop', 'Drop'),
        ('pickup', 'Pickup'),
    )
    drop_pickup = models.CharField(max_length=10, choices=DROP_PICKUP_CHOICES)
    description_id = models.CharField(max_length=100)  #problematic
    name = models.CharField(max_length=1000)
    location = models.CharField(max_length = 100)
    EXPIRY_CHOICES = (
        ('expirable', 'Expirable or Perishable'),
        ('non_expirable', 'Not Expirable or Non Perishable'),
    )
    will_expire = models.CharField(max_length=25, choices=EXPIRY_CHOICES)
    STATUS_CHOICES = (
        ('live', 'Live'),
        ('delivered', 'Delivered'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='live')
    quantity = models.CharField(max_length=25, default='1')
    created_at = models.DateTimeField(default=timezone.now)


    

# from provider.models import post


# new_post = post(
#     user_id=1,
#     photo='/statics/provider/postpics/pizza.jpeg',
#     category='toys',
#     description_id='d110',
#     name='Buzz LightYear',
#     location='Delhi, India',
#     drop_pickup='drop',
#     will_expire='expirable'
# )
# new_post.save()