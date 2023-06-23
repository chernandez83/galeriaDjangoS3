from django.shortcuts import render, redirect

from django.conf import settings

from .models import Image
from .forms import UploadFileForm

from AWS import upload_image

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.cleaned_data['file']
            
            if upload_image(bucket=settings.BUCKET, imagefile_key=file._name,image_file=file):
            
                image = Image.objects.create(
                    name=file._name,
                    content_type=file.content_type,
                    size=file.size,
                    bucket=settings.BUCKET,
                    key=file._name
                )
                
                print(image)
                print(image.__dict__)
            
            return redirect('albums:list')
        