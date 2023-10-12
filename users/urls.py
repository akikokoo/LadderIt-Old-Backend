from django.urls import path
from .views import (
    ContactFormView,
    LoginView,
    RegistrationView
)

urlpatterns = [
    path("",ContactFormView.as_view(), name="contact-form"),
    path('login/',LoginView.as_view(), name="login"),
    path('register/',RegistrationView.as_view(), name="register"),
]