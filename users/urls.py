from django.urls import path
from .views import (
    ContactFormView,
    LoginView
)

urlpatterns = [
    path("",ContactFormView.as_view(), name="contact-form"),
    path('login/',LoginView.as_view(), name="login"),
]