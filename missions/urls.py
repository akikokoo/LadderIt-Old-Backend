from django.urls import path
from .views import (
    MissionCreateView,
    MissionCompleteView,
    MissionDeleteView,
    # ChangeIsCompleteView
)

urlpatterns = [
    path("create/",MissionCreateView.as_view(), name="mission-create"),
    path('complete/<int:pk>/',MissionCompleteView.as_view(), name="mission-complete"), # pk is mission_id
    path('delete/<int:pk>/',MissionDeleteView.as_view(), name="mission-delete"), # pk is mission_id
    # path("isComplete/",ChangeIsCompleteView.as_view(), name="mission-is-complete"),
    

]