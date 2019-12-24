
import os

def addImageToS3(filename, file)
   import boto3
   session = boto3.session.Session(aws_access_key_id='AKIAJOXX6WYXL6SGEPDA',
                     aws_secret_access_key='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')
   s3 = session.resource('s3')
   s3.Bucket(os.environ.get('BUCKET')).put_object(Key='jusitn kke.jpg', Body=request.FILES.get('image'), ACL='public-read')


   # http://tangmingli2.s3.us-east-1.amazonaws.com/tangmingli2/upload-file
   # http://tangmingli2.s3.us-east-1.amazonaws.com/