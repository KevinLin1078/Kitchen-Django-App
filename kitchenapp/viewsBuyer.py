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

from .serializer import DishSerialize, KitchenSerializer, CartSerializer
from django.http import JsonResponse

def get_response(request, table):
   kitchen_session = KitchenSession(request)
   user = kitchen_session.is_login()
   table['status'] = 'ok'
   table['login'] = user[0]
   table['username'] = user[1]
   table['provider'] = kitchen_session.isProvider()
   response = JsonResponse(table) 
   return response

class AllKitchenView(APIView):
   
   def get(self, request):
      # return render(request, 'buyer_kitchen.html', {'kitchens':kitchens, 'login': user[0], 'username':user[1], 'provider': kitchen_session.isProvider()  })
      # return redirect('http://18.222.73.77:8000/')
      kitchens = Kitchen.objects.all()
      serialize = KitchenSerializer(kitchens,  many=True)
      data = {'kitchens': [] }
      for kitchen in kitchens:
         data['kitchens'].append({ 'id': kitchen.id, 'kitchen_name': kitchen.kitchen_name, 'image_url' : kitchen.image_url, 'username': kitchen.provider.username  })
      response = get_response(request, data)
      return response
   
class CartView(APIView):
   @login_required
   def get(self, request):
      print("CART IS => ",request.session.get('user'))
      # return render(request, 'cart.html', {'in_cart': True ,'name': 'Shopping Cart','cart':cart, 'login':user[0], 'username': user[1], 'provider': kitchen_session.isProvider() , 'total': kitchen_session.getShopingCartTotal(), 'cart_length': len(cart) })
      kitchen_session = KitchenSession(request)
      cart = Cart.objects.filter(user=KitchenSession(request).getUserObject(), purchased=False )
      data = { 'cart': [], 'in_cart': True, 'total': kitchen_session.getShopingCartTotal(), 'cart_length': len(cart) }
      for item in cart:
         data['cart'].append({ 'id': item.id, 'dish_name': item.dish.dish_name, 'price': item.dish.price, 'kitchen_name' : item.dish.kitchen.kitchen_name}  )
      response = get_response(request, data)

      return response

class MenuView(APIView):

   def get(self, request, kitchen_id):
      kitchen_session = KitchenSession(request)
      kitchen = kitchen_session.getKitchenObject(kitchen_id)
      dishes = Menu.objects.filter(kitchen=kitchen)
      data = {'dishes': [], 'kitchen_name': kitchen.kitchen_name }
      for dish in dishes:
         data['dishes'].append({'id': dish.id, 'dish_name' : dish.dish_name, 'price': dish.price, 'is_vegan':dish.is_vegan })
      return get_response(request, data)
      

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
      return JsonResponse({'status': "ok"})


class OrderView(APIView):
   @login_required
   def get(self, request):
      kitchen_session = KitchenSession(request)
      orders = Order.objects.filter(user=kitchen_session.getUserObject())
      data = {'orders': [], 'name': "Orders"}
      for order in orders:
         data['orders'].append({'id': order.id, 'price':order.price})

      return get_response(request, data)

class PurchasedOrder(APIView):
   @login_required
   def get(self, request, order_id):
      kitchen_session = KitchenSession(request)
      order = Order.objects.get(id=order_id)
      cart = order.purchased_list.all()
      data = {'cart':[], 'price': order.price, 'order_id' : order_id, 'name':'Order #' }
      for item in cart:
         data['cart'].append({'dish_name':item.dish.dish_name, 'price': item.dish.price, 'kitchen_name':item.dish.kitchen.kitchen_name })
      return get_response(request, data)


class RemoveDish(APIView):
   @login_required
   def post(self, request, cart_id):
      print('REMOVING DISH..... => ', cart_id)
      kitchen_session = KitchenSession(request)
      user = kitchen_session.getUserObject()
      Cart.objects.get(user=user, id=cart_id).delete()

     
      return JsonResponse({'status':'ok',  'total': kitchen_session.getShopingCartTotal()})


