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


def rename_file(bucket, new_mediafile_key, old_mediafile_key):
    try:
        s3 = boto3.resource('s3')

        s3.Object(bucket, new_mediafile_key).copy_from(
            CopySource=bucket+'/'+old_mediafile_key
        )
        s3.Object(bucket, old_mediafile_key).delete()

        s3.Object(bucket, new_mediafile_key).Acl().put(ACL='public-read')

        return True

    except Exception as error:
        print(error)


def delete_file(bucket, file_key):
    try:
        s3 = boto3.resource('s3')
        s3.Object(bucket, file_key).delete()

        return True

    except Exception as error:
        print(error)


def get_mediafile_content(bucket, mediafile_key):
    try:
        s3 = boto3.client('s3')
        
        data = s3.get_object(Bucket=bucket, Key=mediafile_key)
        
        return data['Body'].read()

    except Exception as error:
        print(error)