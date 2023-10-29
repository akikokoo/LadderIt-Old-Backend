from .models import Mission

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
        user = self.request.user
        data = self.request.data

        data["user"] = user.id
        
        serializer = MissionCreateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#NOT DONE (urlde mission_id olmalı mı??)
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


#NOT DONE(TOKEN AND NFT MINTING?)
class MissionCompleteView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions
    
    def post(self, request):
        missions = self.get_queryset()

        mission_id = self.request.data["mission_id"]
        for mission in missions:
            if mission.id == mission_id:
                specified_mission = mission
                
        if specified_mission:
            specified_mission.isCompleted = True
            specified_mission.prevDate = datetime.datetime.utcnow() + datetime.timedelta(hours=int(specified_mission.timeZone))
            specified_mission.numberOfDays += 1
        
            serializer = MissionIsCompletedSerializer(specified_mission, many=True)

            return Response(serializer.data)

        else:
            return Response({"message": "Mission not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        #mint_token(mission)

        
