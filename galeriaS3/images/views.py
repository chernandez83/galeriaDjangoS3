from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from django.conf import settings

from .models import Image
from .forms import UploadFileForm

from albums.models import Album

from AWS import upload_image, delete_file

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


def update(request, pk):
    image = get_object_or_404(Image, pk=pk)
    
    if request.method == 'POST':
        new_name = request.POST.get('name', None)
        if new_name is not None:
            image.set_name(new_name)
    
    return JsonResponse(
        {
            'id': image.id,
            'name': image.title,
            'url': image.url,
        }
    )


def show(request, pk):
    image = get_object_or_404(Image, pk=pk)
    
    return JsonResponse({
        'id': image.id,
        'name': image.name,
        'delete_url': reverse('images:delete', kwargs={'pk': image.pk})
    })


def delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    album = image.album
    
    if delete_file(image.bucket, image.key):
        image.delete()
    
    return redirect('albums:detail', album.id)