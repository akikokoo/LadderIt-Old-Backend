from .models import Mission, User

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
from datetime import timedelta, datetime, timezone


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
                    # Add other properties as needed
                },
                required=['local_time'],
        ),
        responses={201: 'CREATED', 400:'BAD REQUEST'},
    )
    def post(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        local_time = datetime.fromisoformat(self.request.data.get("local_time"))

        # Checking if there is any mission deleted before
        if user.lastMissionDeletionDate:
            nextMissionCreationDate = user.lastMissionDeletionDate + timedelta(days=1)
            # Next mission creation date is one day after the last mission deletion date
            # If the user hasn't passed next mission creation date yet he/she cannot create a new mission.
            if nextMissionCreationDate > local_time:
                return Response({'message': 'Cannot add new mission unless 1 day has passed since you deleted the last mission.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        
        data = self.request.data
        data._mutable = True
        data["startDate"] = local_time
        data._mutable = False
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class MissionDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions
    
    def perform_destroy(self, instance):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        local_time = self.request.data.get("local_time")
        deletionTime = datetime.fromisoformat(local_time)
        user_serializer = UserSerializer(user, data={'lastMissionDeletionDate': deletionTime})
        
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            instance.delete()

    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'local_time': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Local time in ISO 8601 format (e.g., "2023-01-13T21:00:00.000")'
                    ),
                    # Add other properties as needed
                },
                required=['local_time'],
        ),
        responses={200: 'OK'},
    )
    def delete(self, request, *args, **kwargs):
        missions = self.get_queryset()
        mission_id = self.kwargs.get('pk')

        try:
            mission = missions.get(id=mission_id)
            self.perform_destroy(mission)
            return Response({"message": "Mission deleted succesfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": f"Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)



#NOT DONE(TOKEN AND NFT MINTING?)
class MissionCompleteView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'local_time': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Local time in ISO 8601 format (e.g., "2023-01-13T21:00:00.000")'
                    ),
                    # Add other properties as needed
                },
                required=['local_time'],
        ),
        responses={200: 'OK', 400: 'BAD REQUEST'},
    )
    def patch(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        missions = self.get_queryset()
        mission_id = self.kwargs['pk']
        local_time = datetime.fromisoformat(self.request.data.get("local_time")) #request body should include "local_time", write request body req. for swagger doc.

        try:
            mission = missions.get(id=mission_id)

            # numberOfDays is not 0
            if mission.prevDate:
                nextMissionCompletionDate = datetime(year=mission.prevDate.year,
                                                    month=mission.prevDate.month,
                                                    day=mission.prevDate.day+1,
                                                    hour=0,
                                                    minute=0,
                                                    second=0,
                                                    microsecond=0,
                                                    tzinfo=timezone.utc).replace(tzinfo=None)
                
                # User skipped one or more day for the mission completion
                if timedelta(days=1) < (nextMissionCompletionDate - (local_time)):
                    mission.delete() #does that actually deletes the mission?
                    return Response({'message':'Have not completed the mission more than one day!'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Previous completion of that mission is not in the same day with this completion request
                elif nextMissionCompletionDate <= local_time:
                    mission.isCompleted = True
                    mission.prevDate = local_time
                    mission.numberOfDays += 1

                    mission.save()
                    
                    return Response({'message':'Completed the mission successfully!'}, status=status.HTTP_200_OK)
                
                # There is a previous completion on that day
                elif mission.isCompleted == True:
                    return Response({'message':'Cannot complete same mission more than once in a day!'}, status=status.HTTP_400_BAD_REQUEST)
                
            # numberOfDays is 0, because prevDate does not exist.
            else:
                
                mission.isCompleted = True
                mission.prevDate = local_time
                mission.numberOfDays += 1

                mission.save()
                #mint_token(mission) TOKEN MINTING
                
                return Response({'message':'Completed the mission successfully!'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Caught an exception: {e}")
        # given mission_id does not exist
        except:
            return Response({"message":"given mission_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
        
class ChangeIsCompleteView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = User.objects.get(id = self.request.user.id)
        #updating every isCompleted to False for every mission for that user
        Mission.objects.filter(user=user).update(isCompleted=False)
        
        return Response({"message":"Resetted missions correctly"}, status=status.HTTP_200_OK)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ChangeIsCompleteView, cls).as_view(**initkwargs)
        
        # Apply swagger_auto_schema to the post method
        view.post = swagger_auto_schema(
            request_body=None, method="patch")

        return view

        
