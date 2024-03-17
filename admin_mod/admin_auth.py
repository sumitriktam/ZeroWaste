from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

import hashlib
import logging

logger = logging.getLogger(__name__)

class CustomBackend1(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        User = get_user_model() 
        try:
            admin = User.objects.get(is_superuser=True, email=email)
            print(admin.password)
            if check_password(password, admin.password):
                logger.info(f"Admin user '{email}' authenticated successfully.")
                return admin
            else:
                logger.warning(f"Failed login attempt for admin user '{email}' (incorrect password).")
                raise ValidationError("Incorrect email or password.")
        except User.DoesNotExist:
            return None