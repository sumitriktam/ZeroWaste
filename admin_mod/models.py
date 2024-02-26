from django.db import models

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100) 
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
