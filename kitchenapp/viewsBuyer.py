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
      # kitchens = Kitchen.objects.all()
      # kitchen_session = KitchenSession(request)
      # user = kitchen_session.is_login()
      # return render(request, 'buyer_kitchen.html', {'kitchens':kitchens, 'login': user[0], 'username':user[1], 'provider': kitchen_session.isProvider()  })
      # return redirect('http://18.222.73.77:8000/')
      kitchens = Kitchen.objects.all()
      serialize = KitchenSerializer(kitchens,  many=True)
      data = {'status': "ok" ,'kitchens': serialize.data }
      response = get_response(request, data)
      return response
   
class CartView(APIView):
   
   @login_required
   def get(self, request):
      print("CART IS => ",request.session.get('user'))
      # user = kitchen_session.is_login()
      # return render(request, 'cart.html', {'in_cart': True ,'name': 'Shopping Cart','cart':cart, 'login':user[0], 'username': user[1], 'provider': kitchen_session.isProvider() , 'total': kitchen_session.getShopingCartTotal(), 'cart_length': len(cart) })
      kitchen_session = KitchenSession(request)
      cart = Cart.objects.filter(user=KitchenSession(request).getUserObject(), purchased=False )
      serialize = CartSerializer(cart, many=True)
      data={'status': 'ok', 'cart': serialize.data }
      response = get_response(request, data)
      print('Here AT CART COOKIE: GET =>' , request.COOKIES.get('user'))
      
      return response

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


# def get_response(request, table):
#    kitchen_session = KitchenSession(request)
#    user = kitchen_session.is_login()
#    table['login'] = user[0]
#    table['username'] = user[1]
#    table['provider'] = kitchen_session.isProvider()
#    response = JsonResponse(table) 
#    return response

'''
import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from djng.forms import NgModelFormMixin, NgForm
import djng.forms 


class ContactForm(NgModelFormMixin, NgForm):
   form_name = 'contact_form'
   scope_prefix = 'contact_data'
   username  = djng.forms.fields.CharField(max_length=100, required = True)
   password = djng.forms.fields.CharField(max_length=32,  required=True)

class ContactFormView(FormView):
    template_name = 'forms.html'
    form_class = ContactForm
    success_url = reverse_lazy('kitchen:signup')

'''