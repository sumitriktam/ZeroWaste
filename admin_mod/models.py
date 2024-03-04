from django.db import models

import hashlib

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=64)  # Store the hashed password
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

    zerowaste_score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Hash the password using sha256
        if self.password:
            self.password = hashlib.sha256(self.password.encode()).hexdigest()
        super().save(*args, **kwargs)



class Admin(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        # Hash the password using sha256
        if self.password:
            self.password = hashlib.sha256(self.password.encode()).hexdigest()
        super().save(*args, **kwargs)


class Resetpass(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
