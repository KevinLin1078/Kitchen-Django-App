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

class Signup(View):
   def get(self, request):
      form = SignUpForm()
      return render(request, 'forms.html', {'form':form, 'name':'Sign Up'})
   
   def post(self, request):
      form = SignUpForm(request.POST)
      if form.is_valid():
         form.save()
         return HttpResponseRedirect(reverse('kitchen:login'))
         
      return HttpResponseRedirect(reverse('kitchen:signup'))

class Login(View):

   def get(self, request):
      form = LoginForm()
      return render(request, 'forms.html', {'form': form, 'name':'Login'})

   def post(self, request):
      form = LoginForm(request.POST)

      if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']
         if authenticate_user(request, username, password):
            return HttpResponseRedirect(reverse('kitchen:index'))
         
      return HttpResponseRedirect(reverse('kitchen:login'))

class Logout(View):
   
   def get(self, request):
      kitchen_session = KitchenSession(request)
      kitchen_session.removeAll()   
      return HttpResponseRedirect(reverse('kitchen:index')) 



'''
      print('---------->> ',request.FILES.get('image').content_type)
      kitchen_name = request.POST.get('kitchen_name')
      file = request.FILES.get('image')
      filename = file.name
      fileExtension = '.' + filename.split(".")[1].lower()
      print(fileExtension)
      print(kitchen_name)
'''