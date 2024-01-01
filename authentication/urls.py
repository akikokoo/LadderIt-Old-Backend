from django.urls import path, include
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView
)

urlpatterns = [
    path('get_token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]