from django.test import TestCase
from .models import Kitchen, User



class DatabaseTest(TestCase):
    def setUp(self):
        pass
    def test_database_connection(self):
        pass
    

class UserTest(TestCase):
    def setUp(self):
        username, first_name, last_name,password, question_1, answer_1, question_2, answer_2, is_provider = 'username1', 'ivy', 'blue', '1234', 'q1', 'a1','q2', 'a2', True
        User.objects.create(username=username, first_name=first_name, last_name=last_name,password=password, question_1=question_1, answer_1=answer_1, question_2=question_2, answer_2=answer_2, is_provider=is_provider)
        
    def test_add_user(self):
        user1 = User.objects.get(username='username1')
        self.assertEqual(user1.username, 'username1');        


class KitchenTest(TestCase):
    def setUp(self):
        pass

    def test_kitchen_name(self):
        kitchen = Kitchen.objects.get(id=2)
        self.assertEqual(kitchen.kitchen_name, 'Pizza')
        
