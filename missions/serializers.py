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
            "title",
            "description"
        ]

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["id", "title", "numberOfDays", "isCompleted"]
# class PersonListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = ('foo', 'bar',)

#     def to_representation(self, instance):
#         data = super(PersonListSerializer, self).to_representation(instance)
#         data.update(...)
#         return data