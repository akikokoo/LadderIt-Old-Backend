from django.contrib.auth import authenticate
from django.core.mail import send_mail

#REST_FRAMEWORK
from rest_framework import views
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

#SERIALIZERS
from .serializers import ContactFormSerializer


class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error':'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'message':'Successfully logged in'}, status=status.HTTP_200_OK)
        

class ContactFormView(generics.GenericAPIView):   
    serializer_class = ContactFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
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