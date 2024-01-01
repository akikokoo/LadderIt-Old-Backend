from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordBackend(ModelBackend):
    def authenticate(self, request, password=None, **kwargs):        
        try:
            user = User.objects.get(password=password)
        except User.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None