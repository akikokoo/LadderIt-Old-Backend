from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User

#REST_FRAMEWORK
from rest_framework.views import APIView
from rest_framework import views
from rest_framework.response import Response
from rest_framework import generics, status

#SERIALIZERS
from .serializers import (
    ContactFormSerializer,
    UserRegisterSerializer,
    UserDetailSerializer
)

class RegistrationView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#NOT DONE
class UserDetailView(APIView):
    serializer_class = UserDetailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactFormView(generics.GenericAPIView):   
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
                'Name: ' + name + 'Surname: ' + surname + 'Gender: '+ gender +  '\nEmail: ' + email + '\nMessage: ' + message,
                email,
                ['laddergatherit@gmail.com']
            )
            
            # Return a successful response
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)

        else:
            # Return an error response
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)