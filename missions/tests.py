from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class MissionsTestCase(APITestCase):
    def authenticate(self):
        response = self.client.post(
            reverse("register"), #register
            {   
                "username": "akif",
                "password": "kertenkelebek61",
                "wallet":"123",
                "email":"",
                
            },
        )
        
        response = self.client.post(
            reverse("token_obtain_pair"), #login
            {   
                "wallet":"123",
                "password": "kertenkelebek61",
            },
        )
        # print(response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")  

    def test_mission_creation(self):
        '''
        CONDITIONS FOR MISSION CREATION:
            1) Checking if there is any mission deleted before
                1.1) If the user hasn't passed next mission creation date(1 day after last mission deletion date) yet he/she cannot create a new mission.
        '''
        self.authenticate()

    #     # print("-----MISSION CREATION TEST START-----")

        sample_data = {"title": "Görev 1", "user":1, "category":"art", "local_time":"2024-01-19T19:00:00.000", "timezone":"Europe/Istanbul"}
        response = self.client.post(reverse("mission-create"), data=json.dumps(sample_data), content_type='application/json')       
    #     print(response.data)
    #     # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # self.assertEqual(response.data["title"], sample_data["title"])
        # sample_data = {"title": "Görev 1", "user":1, "category":"art", "local_time":"2024-01-20T19:00:00.000", "timezone":"Europe/Istanbul"}
        # response = self.client.post(reverse("mission-create"), sample_data)
        print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["title"], sample_data["title"])
    #     print(response.data["title"])
        
    #     print("-----MISSION CREATION TEST END-----")

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
        sample_data = {"user": 1, "local_time":'2024-01-19T19:00:00.000', "timezone":"Europe/Istanbul"}
        response = self.client.patch(reverse("mission-complete", kwargs={"pk":1}), sample_data)
        print(response.data)


        # sample_data = {"user": 1, "local_time":'2024-01-19 20:00:00.000', "timezone":"Europe/Istanbul"}
        # response = self.client.patch(reverse("mission-complete", kwargs={"pk":1}), sample_data)
        # print(response.data)

    def test_mission_list(self):
        self.authenticate()
        # self.test_mission_creation()
        self.test_mission_complete()
        self.test_mission_complete()
        response = self.client.get(reverse("mission-list"), {"timezone":"Europe/Istanbul", "local_time":"2024-01-19T19:00:00.000"})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mission_delete(self):
        self.authenticate()
        self.test_mission_creation()
        sample_data = {"timezone":"Europe/Istanbul", "local_time":"2024-01-19T19:00:00.000"}
        response = self.client.delete(reverse("mission-delete", kwargs={"pk":1}),data=sample_data)
        
        print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.test_mission_creation()


    
        
        

