from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User
from missions.models import Mission

#REST_FRAMEWORK
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics, status

#SERIALIZERS
from .serializers import (
    ContactFormSerializer,
    UserRegisterSerializer,
    UserDetailSerializer,
)


class RegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions

    def get(self, request, *args, **kwargs):
        user = self.request.user

        missions = self.get_queryset()
        serializer = self.get_serializer(missions, many=True)

        response_data = {
            'username': user.username,
            'missions': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ContactFormView(generics.GenericAPIView):  
    permission_classes = [permissions.AllowAny]
    authentication_classes = [] 
    serializer_class = ContactFormSerializer
    throttle_scope = "send_mail"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            surname = serializer.validated_data['surname']
            email = serializer.validated_data['email']
            gender = serializer.validated_data['gender']
            message = serializer.validated_data['message']

            send_mail(
                'Contact form submission',
                'Name: ' + name + ' Surname:  ' + surname + ' Gender:  '+ gender +  '\nEmail:  ' + email + '\nMessage:  \n' + message,
                email,
                ['fika61ts@gmail.com'], fail_silently=True
            )
            
            # Return a successful response
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)

        else:
            # Return an error response
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)