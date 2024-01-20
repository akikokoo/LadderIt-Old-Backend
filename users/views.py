from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User
from missions.models import Mission

#REST_FRAMEWORK
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#SWAGGER
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#SERIALIZERS
from .serializers import (
    ContactFormSerializer,
    UserRegisterSerializer,
    UserDetailSerializer,
    ProfileUpdateSerializer,
    MissionListSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
)

# OTHERS
import string, random

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

#--------------------------------------------------------------------------------------------------------
class MissionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MissionListSerializer
    
    def get_queryset(self):
        user = self.request.user
        missions = Mission.objects.filter(user=user)

        return missions

    def get(self, request, *args, **kwargs):
        missions = self.get_queryset()
        serializer = self.get_serializer(missions,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserDetailView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)

        serializer = self.get_serializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------------------------


class ProfileUpdateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def patch(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)

        serializer = self.get_serializer(instance=user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            # Return an error response
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(ProfileUpdateView, cls).as_view(**initkwargs)
        
        # Apply swagger_auto_schema to the post method
        view.post = swagger_auto_schema(
            request_body=ProfileUpdateSerializer, method="post")

        return view

# ------------------------------------------------------------------------------------------------------
class PasswordResetView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Email of the user'
                    ),
                    # Add other properties as needed
                },
                required=['email'],
        ),
        responses={
        200: openapi.Response(
            description='Custom Response Body',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING,),
                },
            ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            email = self.request.data.get("email")
            if User.objects.get(email=email):
                token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                send_mail(
                        subject='Password Reset Token',
                        message=f""" To reset your password, please use the following 6-digit token: {token}, 
                        This token is valid for a limited time period. Please use it to reset your password as soon as possible.

                        Thank you,
                        Ladder It Development Team""",
                        from_email='laddergatherit@gmail.com',
                        recipient_list=[email], fail_silently=True
                )

                return Response({"token":token},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'password': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='New password of the user'
                    ),
                    # Add other properties as needed
                },
                required=['email'],
        ),
        responses={
        200: openapi.Response(
            description='Custom Response Body',
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            password = self.request.data.get("password")
            email = self.request.data.get("email")
            user = User.objects.get(email=email)

            user.set_password(password)
            user.save()
        
        except Exception as e:
            return Response({"message":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":"Password has changed successfully"}, status=status.HTTP_200_OK)
        
# ------------------------------------------------------------------------------------------------------


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