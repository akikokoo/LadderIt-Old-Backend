from rest_framework import serializers
from .models import User
from missions.models import Mission

class ContactFormSerializer(serializers.Serializer):
    gender = serializers.CharField(max_length=10)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=20)
    surname = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=1000)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["id", "title", "prevDate", "numberOfDays", "isCompleted"]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email"]