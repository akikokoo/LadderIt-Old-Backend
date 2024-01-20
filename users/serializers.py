from rest_framework import serializers
from .models import User
from missions.models import Mission
from django.contrib.auth.hashers import make_password

class ContactFormSerializer(serializers.Serializer):
    gender = serializers.CharField(max_length=10)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=20)
    surname = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=1000)

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id']
        
class PasswordResetConfirmSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['password', 'id', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'wallet', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserRegisterSerializer, self).create(validated_data)
    
    def to_representation(self, instance):
        # Exclude 'password' field from the serialized data
        data = super().to_representation(instance)
        data.pop('password', None)
        return data
    


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class MissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["id", "title", "prevDate", "numberOfDays", "isCompleted", "startDate", "category"]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]