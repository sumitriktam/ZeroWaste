from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=300) 
    location = models.CharField(max_length=255)
    ROLE_CHOICES = [
        ('receiver', 'Receiver'),
        ('provider', 'Provider'),
        ('enduser', 'End User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Admin(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
