from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
# models
from .models import User, Kitchen, WorkingDay, Menu
from .forms import SignUpForm, LoginForm, AddDishForm, AddKitchenForm
from .session import KitchenSession
from .authenticate import login_required, authenticate_user, seller_required, addToBucket
import boto3
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

class AddKitchen(APIView):
   
   # @login_required
   # @seller_required
   # def get(self, request):
   #    kitchen_session = KitchenSession(request)
   #    form = AddKitchenForm()
   #    user = kitchen_session.is_login()

   #    return render(request, 'forms.html', {'name':'Add Kitchen', 'form': form, 'provider': True, 'login': user[0], 'username':user[1]})

   @login_required
   @seller_required
   def post(self, request):
      form = request.data
      pp = request.POST
      kitchen_name = form['kitchen_name']
      file = form['image']
      print('==============================', pp)
      print('==============================', file)
      image_url = 'https://tangmingli2.s3.us-east-1.amazonaws.com/' + addToBucket(kitchen_name, file)

      kitchen_session = KitchenSession(request)
      Kitchen.objects.create(kitchen_name=kitchen_name, image_url=image_url, provider=kitchen_session.getUserObject())

      return JsonResponse({'status': 'ok', 'url': image_url})


#/myKitchens
class ProviderKitchenView(APIView):
   @login_required
   @seller_required
   def get(self, request):
      kitchen_session = KitchenSession(request)
      provider = kitchen_session.getUserObject()
      kitchens = Kitchen.objects.filter(provider=provider)
      data={'kitchens': []}
      for kitchen in kitchens:
         data['kitchens'].append({ 'id': kitchen.id, 'kitchen_name': kitchen.kitchen_name, 'image_url' : kitchen.image_url, 'username': kitchen.provider.username  })
      return get_response(request, data)



#My kitchen
class AddDish(APIView):
   # @login_required
   # @seller_required
   # def get(self, request, kitchen_id):
   #    kitchen_session = KitchenSession(request)
   #    kitchen = kitchen_session.getKitchenObject(kitchen_id)
   #    dishes = Menu.objects.filter(kitchen=kitchen)

   #    user = kitchen_session.is_login()

   #    data = {'name':'Add Dish' , 'form': AddDishForm(), 'dishes':dishes, 'provider': kitchen_session.isProvider(), 'kitchen_name': kitchen.kitchen_name, 'login': user[0], 'username':user[1]}
   #    return render(request, 'menu.html', data)
   
   @login_required
   @seller_required
   def post(self, request, kitchen_id):
      form = AddDishForm(request.POST)
      if form.is_valid():
         dish_name, price, is_vegan = form.cleaned_data['dish_name'], form.cleaned_data['price'], form.cleaned_data['is_vegan']
         Menu.objects.create(dish_name=dish_name,price=price, is_vegan=is_vegan, kitchen=KitchenSession(request).getKitchenObject(kitchen_id) )
         return JsonResponse({'status': 'ok'})
      return JsonResponse({'status':'error'})

         

  







