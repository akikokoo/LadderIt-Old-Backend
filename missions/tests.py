from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Mission

User = get_user_model()

class MissionsTestCase(APITestCase):
    def authenticate(self):
        self.client.post(
            reverse("register"), #register
            {   
                "username": "akif",
                "password": "123",
                "wallet":"123",
                "email":"akif@hotmail.com",
                
            },
        )

        response = self.client.post(
            reverse("token_obtain_pair"), #login
            {   
                "wallet":"123",
                "password": "123",
            },
        )
        
        try:
            print(response.data)
            token = response.data["access"]
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        except Exception as e:
            print(f"{e}")    

    def test_mission_creation(self):
        '''
        CONDITIONS FOR MISSION CREATION:
            1) Checking if there is any mission deleted before
                1.1) If the user hasn't passed next mission creation date(1 day after last mission deletion date) yet he/she cannot create a new mission.
        '''
        self.authenticate()

        print("-----MISSION CREATION TEST START-----")

        sample_data = {"title": "Görev 1", "user":1, }
        response = self.client.post(reverse("mission-create"), sample_data)       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], sample_data["title"])

        sample_data = {"title": "Görev 2", "user":1}
        response = self.client.post(reverse("mission-create"), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], sample_data["title"])
        print(response.data["title"])
        
        print("-----MISSION CREATION TEST END-----")

    def test_mission_complete(self):
        '''
        CONDITIONS FOR MISSION COMPLETION:
            1) Given mission_id exists
                1.1) 'numberOfDays' is not 0
                    1.1.1) User skipped one or more day for the mission completion
                    1.1.2) Previous completion of that mission is not in the same day with this completion request
                    1.1.3) There is a previous completion on that day
                1.2) 'numberOfDays' is 0, because prevDate does not exist.
            2) Given mission_id does not exist
        '''
        self.authenticate()
        self.test_mission_creation()
        sample_data = {"user": 1, "local_time":'2024-01-19 19:00+0100'}
        response = self.client.patch(reverse("mission-complete", kwargs={"pk":1}), sample_data)
        print(response.data)


        response = self.client.patch(reverse("mission-complete", kwargs={"pk":1}), sample_data)
        print(response.data)

    def test_mission_delete(self):
        self.authenticate()
        self.test_mission_creation()
        response = self.client.delete(reverse("mission-delete", kwargs={"pk":1}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        # self.test_mission_creation()

    def test_changing_is_complete(self):
        self.authenticate()
        self.test_mission_creation()
        response = self.client.patch(reverse("mission-is-complete"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(Mission.objects.get(id=1).isCompleted)

        # can we complete mission after changing isCompleted to False?
        self.test_mission_complete()
        
        

