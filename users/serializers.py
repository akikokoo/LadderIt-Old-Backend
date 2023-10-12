from rest_framework import serializers
from .models import User

class ContactFormSerializer(serializers.Serializer):
    gender = serializers.CharField(max_length=10)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=20)
    surname = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=1000)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[
            "username",
            "password",
        ]

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[
            "first_name",
            "last_name",
            "username",
            "password"
        ]
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user