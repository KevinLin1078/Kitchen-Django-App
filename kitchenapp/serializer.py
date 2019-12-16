from rest_framework import serializers

from .models import Kitchen

class DishSerialize(serializers.Serializer):
   dish_id = serializers.CharField(max_length=10)

class KitchenSerializer(serializers.ModelSerializer):
   class Meta:
      model = Kitchen
      fields = '__all__'

class LoginSerializer(serializers.Serializer):
   username = serializers.CharField(max_length=200)
   password = serializers.CharField(max_length=200)