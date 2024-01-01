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
        fields = ['id', 'username', 'timeZone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.save()
        return user
    
    def to_representation(self, instance):
        # Exclude 'password' field from the serialized data
        data = super().to_representation(instance)
        data.pop('password', None)
        return data
    


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "timeZone"]

class MissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["id", "title", "prevDate", "numberOfDays", "isCompleted"]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]