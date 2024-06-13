from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .restaurants.models import Restaurant

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Restaurant.objects.get(email=email)
            if user.check_password(password):
                return user
        except Restaurant.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Restaurant.objects.get(pk=user_id)
        except Restaurant.DoesNotExist:
            return None
