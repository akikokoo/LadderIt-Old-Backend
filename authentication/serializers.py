from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'password': attrs.get("password"),
        }

        user = authenticate(request=self.context['request'], **credentials)
        if user is None:
            raise serializers.ValidationError("Invalid password")

        refresh = RefreshToken.for_user(user) 
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        data["username"] = user.username 

        return data