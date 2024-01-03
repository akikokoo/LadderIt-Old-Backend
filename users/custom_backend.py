from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordBackend(ModelBackend):
    def authenticate(self, request, password=None, **kwargs):
        if set(request.data.keys()) != {"password"}:
            # If other fields are present, do not authenticate
            return None   

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