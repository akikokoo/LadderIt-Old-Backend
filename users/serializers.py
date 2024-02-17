from rest_framework import serializers
from .models import User
from missions.models import Mission
from django.contrib.auth.hashers import make_password
from datetime import timedelta, datetime
from modules import return_local_time
import pytz
from modules import get_time
from math import ceil
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
            'password': {'write_only': True},
            'username':{'required':True},
            'email':{'required':True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            error_dict = {'errorMessage': 'Username is already taken'}
            raise serializers.ValidationError(error_dict)
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            error_dict = {'errorMessage': 'Email is already taken'}
            raise serializers.ValidationError(error_dict)
        
        return value
    
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
    last_mission_completion_hours = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = ["id", "title", "prevDate", "numberOfDays", "startDate", "category", "last_mission_completion_hours"]
    
    def get_last_mission_completion_hours(self, obj):
        timezone = self.context['request'].query_params.get('timezone')
        local_time = local_time=pytz.timezone(timezone).localize(datetime.fromisoformat(self.context['request'].query_params.get('local_time')))
        prevDate = get_time(timezone, obj.prevDate)

        if prevDate is None:
            return None
        
        # local_time = return_local_time(local_time=local_time,
        #                                current_utc_offset=local_time.strftime("%z")[:3],
        #                                 mission_start_or_deletion_utc=prevDate.strftime("%z")[:3])
        
        last_mission_completion_hours = datetime(year=prevDate.year,
                                                month=prevDate.month,
                                                day=prevDate.day+2,
                                                hour=0,
                                                minute=0,
                                                second=0,
                                                microsecond=0
                                                ) - datetime.now(pytz.UTC).replace(tzinfo=None)
        last_mission_completion_hours = ceil(last_mission_completion_hours.total_seconds() / 3600)
        return last_mission_completion_hours

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]