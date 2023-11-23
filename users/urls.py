from django.urls import path
from .views import (
    ContactFormView,
    RegistrationView,
    MissionListView,
    ProfileUpdateView,
    UserDetailView
)

urlpatterns = [
    path("contact/",ContactFormView.as_view(), name="contact-form"),
    path('register/',RegistrationView.as_view(), name="register"),
    path('user_detail/',UserDetailView.as_view(), name="user-detail"),
    path('mission_list/',MissionListView.as_view(), name="mission-list"),
    path('profile_update/',ProfileUpdateView.as_view(), name="user-profile-update"),
]