from django.db import models
# Create your models here.


class User(models.Model):
   username = models.CharField(max_length=30, null=False)
   first_name = models.CharField(max_length=20, null=False)
   last_name = models.CharField(max_length=20, null=False)
   password = models.CharField(max_length=10, null=False)
   question_1 = models.CharField(max_length=100, default='NA', null=False)
   answer_1 = models.CharField(max_length=20, null=False, default='NA')
   question_2 = models.CharField(max_length=100, default='NA', null=False)
   answer_2 = models.CharField(max_length=20, null=False, default='NA')
   is_provider = models.BooleanField(default=False)

   def setProviderTrue(self):
      self.is_provider = True
   
   def setProviderTrue(self):
      self.is_buyer = True


class Kitchen(models.Model):
   kitchen_name = models.CharField(max_length=50, null=False, default="NA")
   image_url = models.CharField(max_length=200)
   provider = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

class WorkingDay(models.Model):
   day = models.CharField(max_length=15, null=False, default='NA')
   start_time = models.CharField(max_length=10, null=False, default='NA') 
   end_time = models.CharField(max_length=10, null=False, default='NA') 

   kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)

class Menu(models.Model):
   dish_name = models.CharField(max_length=50, null=False, default='NA')
   price =  models.DecimalField(max_digits=10, decimal_places=2, null=False)
   is_vegan = models.BooleanField(default=False)
   kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, null=False)


class KitchenImage(models.Model):
   name = models.CharField(max_length=100, null = False, default='NA')
   image= models.ImageField(upload_to='images/')


class Cart(models.Model):
   user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
   dish = models.ForeignKey(Menu, null=False, on_delete=models.CASCADE)
   purchased = models.BooleanField(default=False)


class Order(models.Model):
   user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
   purchased_list = models.ManyToManyField(Cart)
   price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)