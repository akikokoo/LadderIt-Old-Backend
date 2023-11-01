from rest_framework import serializers
from .models import Mission

class MissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "user",
            "title"
        ]
    

class MissionIsCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "user_id",
            "title"
        ]
