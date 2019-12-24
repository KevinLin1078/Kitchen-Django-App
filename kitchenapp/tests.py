# from django.test import TestCase
import os
# Create your tests here.
print(os.environ.get('AWS_ACCESS_KEY'))


import boto3

# s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_KEY'), aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY'))
# for bucket in s3.buckets.all():
#       print(bucket.all)

################################################
# bucket_name = os.environ.get('BUCKET')
# key = "upload-file"

# s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_KEY'), aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY'))
# bucket = s3.Bucket(bucket_name)
# bucket.upload_file("upload.txt", key)
# location = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_KEY'), aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY')).get_bucket_location(Bucket=bucket_name)
# # url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(location, bucket_name, key)
# print(location)
