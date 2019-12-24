
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Kitchen
from django.urls import reverse
from django.shortcuts import get_object_or_404
import boto3
from django.http import JsonResponse

from django.conf import settings

def seller_required(function):
   def wrapper(*args, **kwargs):
      session = args[1].session.get('user')[2]
      if args[1].session.get('user')[2] == True:
         return function(*args, **kwargs)
      else:
         return HttpResponse("You are not a seller")
   return wrapper


def authenticate_user(request, username, password):
   userObj = None
   try:
      userObj = User.objects.get(username=username, password=password)
      request.session['user'] = (username, password, userObj.is_provider)
      return True
   except Exception:
      return False

def login_required(function):
   def wrapper(*args, **kwargs):
      cookie = args[1].COOKIES
      print("@LOGIN ", cookie)
      username , password= cookie.get('user') ,cookie.get('password')
      if authenticate_user(args[1],  username, password ):
         return function(*args, **kwargs)
      else:
         return JsonResponse({'status': 'error login'})
   return wrapper

import os 
def addToBucket(kitchen_name, file):
      filename = file.name
      fileExtension = '.' + filename.split(".")[1].lower()
      key = str(kitchen_name + fileExtension)
      print("IN ADDDDDD=======> 1111111111111")
      
      print("==NEW====> KEY",settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)

      session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
      print("IN ADDDDDD=======> 222222222222")
      s3 = session.resource('s3')
      print("IN ADDDDDD=======> 3333333333333")
      s3.Bucket('tangmingli2').put_object(Key=key, Body=file, ACL='public-read')
      print("IN ADDDDDD=======> 44444444444")

      # session = boto3.session.Session(aws_access_key_id=os.environ.get('AWS_KEY'), aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY'))
      # s3 = session.resource('s3')
      # print("IN ADDDDDD=======> 222")
      # s3.put(Bucket='tangmingli2', Key=key, Body=file, ACL='public-read')
      # print("IN ADDDDDD=======> 333")

      return key
      


