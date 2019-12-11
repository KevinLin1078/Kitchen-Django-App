from rest_framework import serializers



class DishSerialize(serializers.Serializer):
   dish_id = serializers.CharField(max_length=10)