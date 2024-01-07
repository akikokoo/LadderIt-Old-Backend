from .models import Mission, User

#REST_FRAMEWORK
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#SWAGGER
from drf_yasg.utils import swagger_auto_schema

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

    def post(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)

        # Checking if there is any mission deleted before
        if user.lastMissionDeletionDate:
            nextMissionCreationDate = user.lastMissionDeletionDate + timedelta(days=1)
            print(nextMissionCreationDate)
            # Next mission creation date is one day after the last mission deletion date
            # If the user hasn't passed next mission creation date yet he/she cannot create a new mission.
            if nextMissionCreationDate > datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=int(user.timeZone)):
                return Response({'message': 'Cannot add new mission unless 1 day has passed since you deleted the last mission.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        data = self.request.data

        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MissionCreateView, cls).as_view(**initkwargs)
        
        # Apply swagger_auto_schema to the post method
        view.post = swagger_auto_schema(
            request_body=MissionCreateSerializer, method="post")

        return view
    


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
        deletionTime = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=int(user.timeZone))
        user_serializer = UserSerializer(user, data={'lastMissionDeletionDate': deletionTime})
        
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            instance.delete()

    def delete(self, request, *args, **kwargs):
        missions = self.get_queryset()
        mission_id = self.kwargs.get('pk')

        try:
            mission = missions.get(id=mission_id)
            self.perform_destroy(mission)
            return Response({"message": "Mission deleted succesfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": f"Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)


    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MissionDeleteView, cls).as_view(**initkwargs)
        
        # Apply swagger_auto_schema to the post method
        view.post = swagger_auto_schema(
            request_body = None, method="delete")

        return view


#NOT DONE(TOKEN AND NFT MINTING?)
class MissionCompleteView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions
    
    def patch(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        missions = self.get_queryset()
        mission_id = self.kwargs['pk']

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
                # print(mission.prevDate)
                # print(nextMissionCompletionDate)
                # print(datetime.utcnow() + timedelta(hours=int(user.timeZone)))
                # print(nextMissionCompletionDate - (datetime.utcnow() + timedelta(hours=int(user.timeZone))))
                # User skipped one or more day for the mission completion
                if timedelta(days=1) < (nextMissionCompletionDate - (datetime.utcnow() + timedelta(hours=int(user.timeZone)))):
                    mission.delete() #does that actually deletes the mission?
                    return Response({'message':'Have not completed the mission more than one day!'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Previous completion of that mission is not in the same day with this completion request
                elif nextMissionCompletionDate <= datetime.utcnow() + timedelta(hours=int(user.timeZone)):
                    mission.isCompleted = True
                    mission.prevDate = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=int(user.timeZone))
                    mission.numberOfDays += 1

                    mission.save()

                    return Response({'message':'Completed the mission successfully!'}, status=status.HTTP_200_OK)
                
                # There is a previous completion on that day
                elif mission.isCompleted == True:
                    return Response({'message':'Cannot complete same mission more than once in a day!'}, status=status.HTTP_400_BAD_REQUEST)
                
            #numberOfDays is 0, because prevDate does not exist.
            else:
                
                mission.isCompleted = True
                mission.prevDate = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=int(user.timeZone))
                mission.numberOfDays += 1

                mission.save()
                #mint_token(mission) TOKEN MINTING
                
                return Response({'message':'Completed the mission successfully!'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(f"Caught an exception: {e}")
        # given mission_id does not exist
        except:
            return Response({"message":"given mission_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(MissionCompleteView, cls).as_view(**initkwargs)
        
        # Apply swagger_auto_schema to the post method
        view.post = swagger_auto_schema(
            request_body=None, method="post")

        return view
        
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

        
