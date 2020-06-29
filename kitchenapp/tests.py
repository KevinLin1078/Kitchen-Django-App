from django.test import TestCase
from .models import Kitchen, User


user1 = None    

class UserTest(TestCase):
    
    def setUp(self):
        print('Creating user')
        username, first_name, last_name,password, question_1, answer_1, question_2, answer_2, is_provider = 'username1', 'ivy', 'blue', '1234', 'q1', 'a1','q2', 'a2', True
        User.objects.create(username=username, first_name=first_name, last_name=last_name,password=password, question_1=question_1, answer_1=answer_1, question_2=question_2, answer_2=answer_2, is_provider=is_provider)
        
    def test_add_user(self):
        global user1    
        print('Testing user')
        user1 = User.objects.get(username='username1')
        self.assertEqual(user1.username, 'username1')        
        self.assertTrue(user1.is_provider)

        
class KitchenTest(TestCase):

    def setUp(self):
        print('Adding Kitchen ')
        global user1
        kitchen_name, image_url = 'Pizza', 'http://kitchen_img.s3-website-us-east-1.amazonaws.com/'
        Kitchen.objects.create(kitchen_name=kitchen_name, image_url=image_url, user1)
        

    
    def test_kitchen_name(self):
        print('Testing Kitchen ')
        kitchen = Kitchen.objects.get(id=1)
        self.assertEqual(kitchen.kitchen_name, 'Pizza')
        
