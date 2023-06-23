import boto3


def create_folder(bucket, directory_name):
    try:
        s3 = boto3.client('s3')

        key = directory_name + '/'
        s3.put_object(Bucket=bucket, Key=key)

        return key

    except Exception as error:
        print(error)

def upload_image(bucket, imagefile_key, image_file):
    try:
        s3 = boto3.resource('s3')
        
        bucket = s3.Bucket(bucket)
        
        return bucket.put_object(
            ACL='public-read',
            Key=imagefile_key,
            ContentType=image_file.content_type,
            Body=image_file
        )
        
    except Exception as error:
        print(error)