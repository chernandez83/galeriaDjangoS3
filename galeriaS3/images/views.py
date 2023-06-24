from django.shortcuts import redirect, get_object_or_404

from django.conf import settings

from .models import Image
from .forms import UploadFileForm

from albums.models import Album

from AWS import upload_image

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.cleaned_data['file']
            album = get_object_or_404(Album, id=form.cleaned_data['album_id'])
            
            key = album.key + file._name
            if upload_image(bucket=settings.BUCKET, imagefile_key=key,image_file=file):
            
                image = Image.objects.create(
                    name=file._name,
                    content_type=file.content_type,
                    size=file.size,
                    bucket=settings.BUCKET,
                    key=key,
                    album=album
                )
                
                print(image)
                print(image.__dict__)
            
            return redirect('albums:detail', album.id)
        