from rest_framework import serializers
from .models import Mission
from users.models import User



class MissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            "user",
            "title",
            "category",
        ]
    
    def validate_title(self, value):
        if Mission.objects.filter(title=value).exists():
            error_dict = {
                'errorMessage': 'Title is already taken',
            }
            raise serializers.ValidationError(error_dict)
        return value
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['lastMissionDeletionDate']