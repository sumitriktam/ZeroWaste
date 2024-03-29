from django.db import models
from admin_mod.models import User 
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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

class toysDes(models.Model):
    age_group = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)])
    COND_CHOICES = (
        ('new', 'New'),
        ('mint', 'Mint'),
        ('old','Old'),
    )
    condition = models.CharField(max_length=10, choices=COND_CHOICES)
    desc = models.CharField(max_length=1000, default="")

class groceryDes(models.Model):
    desc = models.CharField(max_length=1000, default="")
    expiry_date = models.DateField()
    expiry_time = models.TimeField()

class clothDes(models.Model):
    desc = models.CharField(max_length=1000, default="")
    GENDER_CHOICES = [
        ('male', 'For Male'),
        ('female', 'For Female'),
        ('both', 'For Both'),
    ]
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    COND_CHOICES = (
        ('new', 'New'),
        ('mint', 'Mint'),
        ('old','Old'),
    )
    condition = models.CharField(max_length=10, choices=COND_CHOICES)
    SIZE_CHOICES = (
        ('s', 'S'),
        ('m', 'M'),
        ('l','L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('other', 'Other'),
    )
    size = models.CharField(max_length=10, choices=COND_CHOICES)

class foodDes(models.Model):
    desc = models.CharField(max_length=1000, default="")
    expiry_date = models.DateField()
    expiry_time = models.TimeField()

class otherDes(models.Model):
    desc = models.CharField(max_length=1000, default="")