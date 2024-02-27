from django.contrib.auth.backends import ModelBackend
from .models import User, Admin
from django.contrib.auth.hashers import check_password

class CustomBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user and check_password(password, user.password):
                return user
            admin = Admin.objects.get(email=email)
            if admin and check_password(password, admin.password):
                return admin
            else:
                return None
        except:
            return None
        


# class CustomBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None):
#         try:
#             user = User.objects.get(email=email)
            
#             if user and check_password(password, user.password):
#                 return user
#             else:
#                 return None
#         except:
#             try:
#                 admin = Admin.objects.get(email=email)
                
#                 if admin and check_password(password, admin.password):
#                     return admin
#                 else:
#                     return None
#             except Admin.DoesNotExist:
#                 return None
#     def checkUser(self, request, email=None):
#             user = User.objects.get(email=email)
#             if user:
#                 return user
#             else:
#                 return None
