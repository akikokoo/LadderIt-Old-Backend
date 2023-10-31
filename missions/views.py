from .models import Mission, User

#REST_FRAMEWORK
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#SERIALIZERS
from .serializers import (
    MissionIsCompletedSerializer,
    MissionCreateSerializer,
)

#OTHER LIBRARIES
import datetime

#DONE
class MissionCreateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)

        if user.lastMissionDeletionDate:
            nextMissionCreationDate = user.lastMissionDeletionDate + datetime.timedelta(days=1)
            if nextMissionCreationDate > datetime.datetime.utcnow() + datetime.timedelta(hours=int(user.timeZone)):
                return Response({'message': 'Cannot create a mission'}, status=status.HTTP_400_BAD_REQUEST)

        data = self.request.data
        data["user"] = user.id

        serializer = MissionCreateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class MissionDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        mission = Mission.objects.filter(user=user)

        return mission
    
    
    def delete(self, request, *args, **kwargs):
        missions = self.get_queryset()
        mission_id = self.kwargs['pk']

        mission = missions.get(mission_id=mission_id)

        mission.delete()

        return Response({"message": "Mission deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)


#NOT DONE(TOKEN AND NFT MINTING?) (urlde mission_id olmalı mı??)
class MissionCompleteView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions
    
    def post(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        missions = self.get_queryset()
        mission_id = self.request.data["mission_id"]

        for mission in missions:
            if mission.id == mission_id:
                specified_mission = mission
        
        # If the given mission_id exists.
        if specified_mission:
            nextMissionCompletionDate = datetime.datetime(year=user.lastMissionDeletionDate.year, month=user.lastMissionDeletionDate.month, day=user.lastMissionDeletionDate.day+1, hour=0, second=0)
            # Previous completion of that mission should not be in the same day with this completion request
            if nextMissionCompletionDate <= datetime.datetime.utcnow() + datetime.timedelta(hours=int(user.timeZone)):
                specified_mission.isCompleted = True
                specified_mission.prevDate = datetime.datetime.utcnow() + datetime.timedelta(hours=int(user.timeZone))
                specified_mission.numberOfDays += 1
            
                serializer = MissionIsCompletedSerializer(specified_mission, many=True)

                # If it is not the day 1, mint token
                if specified_mission.numberOfDays != 1:
                    #mint_token(mission) TOKEN MINTING
                    return Response(serializer.data)
                
                else:
                    return Response(serializer.data)
            
            else:
                return Response({'message':'Cannot complete same mission more than once in a day!'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Mission not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        

        
