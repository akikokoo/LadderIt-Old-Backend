
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # Customize the response data if needed
    def post(self, request, *args, **kwargs):
        password = request.data.get('password', None)

        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request=request, password=password)

        if user is None:
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        response = super().post(request, *args, **kwargs)
        # Customize response data here if needed
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    # Customize the response data if needed
    def post(self, request, *args, **kwargs):
        password = request.data.get('password', None)

        if not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request=request, password=password)

        if user is None:
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        response = super().post(request, *args, **kwargs)
        # Customize response data here if needed
        return response