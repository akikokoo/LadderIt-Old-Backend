from rest_framework import serializers
from .models import Mission
from users.models import User

class MissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "id",
            "user",
            "title"
        ]
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['lastMissionDeletionDate']



