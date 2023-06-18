# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
# Client
import boto3
s3 = boto3.client('s3')
s3.upload_file(<LOCAL_PATH>, <BUCKET_NAME>, <KEY>)

# Resource
import boto3
s3 = boto3.resource('s3')
s3_object = s3.Object(<BUCKET_NAME>, key=<KEY>)
s3_object.upload_file(<LOCAL_PATH>)

# Client
import boto3
s3 = boto3.client('s3')
for obj in s3.list_objects(Bucket=<BUCKET_NAME>)['Contents']:
   print(obj['Key'])

# Resource
s3 = boto3.resource('s3')
bucket = s3.Bucket(<BUCKET_NAME>)
for obj in bucket.objects.all():
    print(obj.key)