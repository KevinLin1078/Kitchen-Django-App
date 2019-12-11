from .models import User, Kitchen, Menu, Cart, Order


class KitchenSession(object):
   
   def __init__(self, request):
      self.session = request.session

   def isProvider(self):
      user = self.session.get('user')
      if user == None:
         return False
      return user[2]
   
   def is_login(self):
      user = self.session.get('user')
      if user :
         return (True, user[0])
      return (False, None)
   
   def getUserObject(self):
      user = self.session.get('user')
      return User.objects.get(username=user[0], password=user[1])

   
   def getKitchenObject(self, kitchen_id):
      return Kitchen.objects.get(id=kitchen_id)

   def getDishObject(self, dish_id):
      return Menu.objects.get(id=dish_id)


   def getShopingCartTotal(self):
      cart = Cart.objects.filter(user=self.getUserObject(), purchased=False)      
      return sum(item.dish.price for item in cart)

   def processTransaction(self):
      cart = Cart.objects.filter(user=self.getUserObject(), purchased=False)  
      order = Order(user=self.getUserObject())
      order.save()
      total = 0
      for item in cart:
         item.purchased=True
         item.save()
         order.purchased_list.add(item)
         total += item.dish.price
      order.price = total
      order.save()

   def add(self, key, value):
      self.session[key] = value

   def remove(self, key, value):
      self.session.pop(key)

   def removeAll(self):
      self.session.clear()



