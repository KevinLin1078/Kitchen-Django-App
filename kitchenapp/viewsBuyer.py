from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
# models
from .models import User, Kitchen, WorkingDay, Menu, Cart, Order
from .forms import SignUpForm, LoginForm, AddDishForm, AddKitchenForm
from .session import KitchenSession
from .authenticate import login_required, authenticate_user, seller_required, addToBucket
import boto3

from .serializer import DishSerialize


class AllKitchenView(APIView):
   
   def get(self, request):
      
      kitchens = Kitchen.objects.all()
      kitchen_session = KitchenSession(request)
      user = kitchen_session.is_login()
      return render(request, 'buyer_kitchen.html', {'kitchens':kitchens, 'login': user[0], 'username':user[1], 'provider': kitchen_session.isProvider()  })
      
      

class CartView(ListView):
   
   @login_required
   def get(self, request):
      kitchen_session = KitchenSession(request)
      cart = Cart.objects.filter(user=KitchenSession(request).getUserObject(), purchased=False )
      user = kitchen_session.is_login()
      return render(request, 'cart.html', {'in_cart': True ,'name': 'Shopping Cart','cart':cart, 'login':user[0], 'username': user[1], 'provider': kitchen_session.isProvider() , 'total': kitchen_session.getShopingCartTotal(), 'cart_length': len(cart) })
      


class MenuView(View):

   def get(self, request, kitchen_id):
      kitchen_session = KitchenSession(request)
      kitchen = kitchen_session.getKitchenObject(kitchen_id)
      dishes = Menu.objects.filter(kitchen=kitchen)
      
      user = kitchen_session.is_login()
      return render(request, 'buyer_menu.html', {'dishes': dishes, 'kitchen_name':kitchen.kitchen_name, 'login': user[0], 'username':user[1],'provider': kitchen_session.isProvider() })
      

class AddToCart(APIView):
   @login_required
   def post(self, request):
      serializer = DishSerialize(data=request.data)
      if serializer.is_valid():
         form = serializer.data
         dish_id = form['dish_id']
         print(dish_id)
         kitchen_session = KitchenSession(request)
         Cart.objects.create(user=kitchen_session.getUserObject(), dish=kitchen_session.getDishObject(dish_id))
         return Response({'status': "OK"})
         
      return Response({'status': "error"})

class Purchase(APIView):
   @login_required
   def post(self, request):
      KitchenSession(request).processTransaction()
      response = Response({'status': "Purchased Successfully"})
      response["Access-Control-Allow-Origin"] = "*"
      return response


class OrderView(View):
   def get(self, request):
      kitchen_session = KitchenSession(request)
      orders = Order.objects.filter(user=kitchen_session.getUserObject())
      user = kitchen_session.is_login()

      return render(request, 'order.html', {'name':'Order' , 'login': user[0], 'username':user[1],'provider': kitchen_session.isProvider(),'orders': orders })


class PurchasedOrder(View):
   @login_required
   def get(self, request, order_id):
      kitchen_session = KitchenSession(request)
      order = Order.objects.get(id=order_id)
      cart = order.purchased_list.all()
      user = kitchen_session.is_login()
      return render(request, 'cart.html', {'in_cart':False, 'price' : order.price, 'order_id' : order_id, 'name':'Order #' , 'login': user[0], 'username':user[1],'provider': kitchen_session.isProvider(), 'purchased': True,'cart':cart })


class RemoveDish(View):
   @login_required
   def get(self, request, cart_id):
      user = KitchenSession(request).getUserObject()
      Cart.objects.get(user=user, id=cart_id).delete()
      return HttpResponseRedirect(reverse('kitchen:shoppingCart'))

