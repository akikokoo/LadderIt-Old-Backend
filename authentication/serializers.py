from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)

class CustomTokenObtainPairSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
       
        self.fields["password"] = PasswordField()
        self.fields["wallet"] = serializers.CharField()

    def validate(self, attrs):
        credentials = {
            'password': attrs.get("password"),
            'wallet': attrs.get("wallet"),
        }

        user = authenticate(request=self.context['request'], **credentials)

        if user is None:
            raise serializers.ValidationError("Invalid wallet address or password")

        refresh = RefreshToken.for_user(user) 
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        data["username"] = user.username 

        return data