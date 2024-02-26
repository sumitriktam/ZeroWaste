from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            
            # Verify the password using your custom method
            if user.password == password:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None