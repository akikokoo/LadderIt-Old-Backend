from .models import Mission, User
from django.db.models import F

#REST_FRAMEWORK
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#SWAGGER
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#SERIALIZERS
from .serializers import (
    MissionCreateSerializer,
    UserSerializer
)

#OTHER LIBRARIES
from datetime import timedelta, datetime
import pytz
from modules import return_local_time, get_time
from .mint import mint_token

class MissionCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class=MissionCreateSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'local_time': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Local time in ISO 8601 format (e.g., "2023-01-13T21:00:00.000")'
                    ),
                    'timezone': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Timezone in IANA format (e.g., "Europe/Istanbul")'
                    # Add other properties as needed
                    )
                    # Add other properties as needed
                },
                required=['local_time'],
        ),
        responses={201: 'CREATED', 400:'BAD REQUEST'},
    )
    def post(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        
        # local_time = self.request.data.get("local_time")
        current_timezone = self.request.data.get("timezone")
        local_time = pytz.timezone(current_timezone).localize(datetime.fromisoformat(self.request.data.get("local_time")))

        # Checking if there is any mission deleted before
        if user.lastMissionDeletionDate:
            # getting local_time in the same timezone with the mission start or deletion date
            deletion_time = get_time(user.deletionTimezone, user.lastMissionDeletionDate)
            nextMissionCreationDate = deletion_time + timedelta(days=1)
            current_time_in_deletion_timezone = get_time(user.deletionTimezone, datetime.now(pytz.UTC))

            # Next mission creation date is one day after the last mission deletion date
            # If the user hasn't passed next mission creation date yet he/she cannot create a new mission.
            if nextMissionCreationDate > current_time_in_deletion_timezone:
                return Response({'errorMessage': 'Cannot add new mission unless 1 day has passed since you deleted the last mission.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                data = self.request.data
                serializer = self.get_serializer(data=data)

                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    instance.startDate = datetime.now(pytz.UTC)
                    instance.startTimezone = current_timezone
                    instance.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = self.request.data
            serializer = self.get_serializer(data=data)

            if serializer.is_valid(raise_exception=True):
                instance = serializer.save()
                instance.startDate = datetime.now(pytz.UTC)
                instance.startTimezone = current_timezone
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class MissionDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'local_time': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Local time in ISO 8601 format (e.g., "2023-01-13T21:00:00.000")'
                    ),
                    'timezone': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Timezone in IANA format (e.g., "Europe/Istanbul")'
                    # Add other properties as needed
                    )
                    # Add other properties as needed
                },
                required=['local_time'],
        ),
        responses={200: 'OK'},
    )
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.request.user.id
        missions = Mission.objects.filter(user=user)
        mission_id = self.kwargs.get('pk')

        user = User.objects.get(id=user_id)
        
        local_time = self.request.data.get("local_time")
        current_timezone = self.request.data.get("timezone")

        deletionTime = datetime.now(pytz.UTC)
        try:
            mission = missions.get(id=mission_id)
            user_serializer = UserSerializer(user, data={'lastMissionDeletionDate': deletionTime, 'deletionTimezone': current_timezone})
        
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                mission.delete()

                return Response({"message": "Mission deleted succesfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"errorMessage": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)



#NOT DONE(TOKEN AND NFT MINTING?)
class MissionCompleteView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'local_time': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Local time in ISO 8601 format (e.g., "2023-01-13T21:00:00.000")'
                    ),
                    'timezone': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Timezone in IANA format (e.g., "Europe/Istanbul")'
                    # Add other properties as needed
                    )
                },
                required=['local_time'],
        ),
        responses={200: 'OK', 400: 'BAD REQUEST'},
    )
    def patch(self, request, *args, **kwargs):
        mission_id = self.kwargs['pk']
        mission = Mission.objects.select_related('user').get(id=mission_id)

        user = mission.user
        user_wallet = user.wallet

        current_timezone = self.request.data.get("timezone")
        local_time = pytz.timezone(current_timezone).localize(datetime.fromisoformat(self.request.data.get("local_time")))
        current_time_in_mission_start_timezone = get_time(mission.startTimezone, datetime.now(pytz.UTC)).replace(tzinfo=None)
        # numberOfDays is not 0
        if mission.prevDate:
            prevDate = get_time(mission.startTimezone, mission.prevDate).replace(tzinfo=None)
            nextMissionCompletionDate = datetime(year=prevDate.year,
                                                month=prevDate.month,
                                                day=prevDate.day+1,
                                                hour=0,
                                                minute=0,
                                                second=0,
                                                microsecond=0
                                                )
            # User skipped one or more day for the mission completion
            if timedelta(days=1, hours=24 - prevDate.hour) < (current_time_in_mission_start_timezone - prevDate):
                mission.delete()
                return Response({'errorMessage':'Have not completed the mission more than one day!'}, status=status.HTTP_400_BAD_REQUEST)
                
            # Previous completion of that mission is not in the same day with this completion request
            elif nextMissionCompletionDate <= current_time_in_mission_start_timezone:
                mission.prevDate = datetime.now(pytz.UTC)
                mission.numberOfDays = F('numberOfDays') + 1

                # mint_token(user_wallet)
                    
                mission.save()
                    
                return Response({'message':'Completed the mission successfully!'}, status=status.HTTP_200_OK)
                
            # There is a previous completion on that day
            else:
                return Response({'errorMessage':'Cannot complete same mission more than once in a day!'}, status=status.HTTP_400_BAD_REQUEST)
                
        # numberOfDays is 0, because prevDate does not exist.
        else:          
            mission.prevDate = datetime.now(pytz.UTC)
            mission.numberOfDays = F('numberOfDays') + 1
            mission.save()

            return Response({'message':'Completed the mission successfully!'}, status=status.HTTP_200_OK)
    
        
# class ChangeIsCompleteView(generics.GenericAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, *args, **kwargs):
#         user = User.objects.get(id = self.request.user.id)
#         #updating every isCompleted to False for every mission for that user
#         missions = Mission.objects.filter(user=user)

#         for mission in missions:
            
#             mission.isCompleted = False
#             mission.save()

#         return Response({"message":"Resetted missions correctly"}, status=status.HTTP_200_OK)

#     @classmethod
#     def as_view(cls, **initkwargs):
#         view = super(ChangeIsCompleteView, cls).as_view(**initkwargs)
        
#         # Apply swagger_auto_schema to the post method
#         view.post = swagger_auto_schema(
#             request_body=None, method="patch")

#         return view
