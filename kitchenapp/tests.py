from django.test import TestCase
from .models import Kitchen



class KitchenTestCase(TestCase):
    def setUp(self):
        pass

    def test_kitchen_name(self):
        kitchen = Kitchen.objects.get(id=2)
        self.assertEqual(kitchen.kitchen_name, 'Pizza')
        
