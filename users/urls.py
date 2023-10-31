from django.urls import path
from .views import (
    ContactFormView,
    RegistrationView,
    UserDetailView
)

urlpatterns = [
    path("contact/",ContactFormView.as_view(), name="contact-form"),
    path('register/',RegistrationView.as_view(), name="register"),
    path('user_detail/',UserDetailView.as_view(), name="user-detail"),

]