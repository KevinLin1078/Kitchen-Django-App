from django.test import TestCase
from .models import Kitchen, User



class DatabaseTest(TestCase):
    def setUp(self):
        pass
    def test_database_connection(self):
        pass
    

class UserTest(TestCase):
    def setUp(self):
        pass
    
    def test_user_creation(self):
        pass


class KitchenTest(TestCase):
    def setUp(self):
        pass

    def test_kitchen_name(self):
        kitchen = Kitchen.objects.get(id=2)
        self.assertEqual(kitchen.kitchen_name, 'Pizza')
        
