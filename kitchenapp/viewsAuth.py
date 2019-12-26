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
from .serializer import SignupSerializer

def get_updated_JsonResponse(request, table):
   kitchen_session = KitchenSession(request)
   user = kitchen_session.is_login()
   table['status'] = 'ok'
   table['login'] = user[0]
   table['username'] = user[1]
   table['provider'] = kitchen_session.isProvider()
   response = JsonResponse(table) 
   response["Access-Control-Allow-Headers"] = "Set-Cookie"
   response['Access-Control-Expose-Headers'] = 'Set-Cookie'
   return response


class Signup(APIView):
   # def get(self, request):
   #    form = SignUpForm()
   #    return render(request, 'forms.html', {'form':form, 'name':'Sign Up'})
   
   def post(self, request):
      serialize = SignupSerializer(data=request.data)
      if serialize.is_valid():
         serialize.save()
         return Response({'status': 'ok'})
      return Response({'status': 'error user not added'})

class Login(APIView):

   def get(self, request):
      print('Cookie is => ',request.COOKIES)
      
      return JsonResponse({"itty": 'bitty'})
   
   def post(self, request):
      print(request.data)
      username = request.data['username']
      password = request.data['password']
               
      if authenticate_user(request, username, password):
         
         response = get_updated_JsonResponse(request, {})
         response.set_cookie('user', username)
         response.set_cookie('password', password)
         return response
         
      return JsonResponse({'status': "errorRest"})

class Logout(APIView):
   
   def post(self, request):
      kitchen_session = KitchenSession(request)
      kitchen_session.removeAll()   
      return JsonResponse({'status': 'ok'}) 



'''
      print('---------->> ',request.FILES.get('image').content_type)
      kitchen_name = request.POST.get('kitchen_name')
      file = request.FILES.get('image')
      filename = file.name
      fileExtension = '.' + filename.split(".")[1].lower()
      print(fileExtension)
      print(kitchen_name)
'''