from django.db import models
from django.contrib.auth.models import User

users = User.objects.filter(email="zerowaste@gmail.com")
for user in users:
    print(user.email)


