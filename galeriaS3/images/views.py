import json
import shutil

from pathlib import Path

from wsgiref.util import FileWrapper

from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.template.loader import get_template

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from .models import Image
from .forms import UploadFileForm

from albums.models import Album

from AWS import upload_image, delete_file, get_mediafile_content, download_file

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
                
                # print(image)
                # print(image.__dict__)
            
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
    
    #if delete_file(image.bucket, image.key):
    #    image.delete()
    
    Image.objects.delete_by_aws(image.id)
    
    return redirect('albums:detail', album.id)


@csrf_exempt
def delete_many(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        ids = payload.get('ids', [])
        
        return JsonResponse({
            'ids': [Image.objects.delete_by_aws(id) for id in ids]
        })


def download(request, pk):
    image = get_object_or_404(Image, pk=pk)
    
    content = get_mediafile_content(image.bucket, image.key)
    
    response = HttpResponse(content, content_type=image.content_type)
    response['Content-Disposition'] = f'attachment; filename={image.name}'
    
    return response


def download_many(request):
    dir_path = 'tmp/images'
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    for id in request.GET.get('ids', '').split(','):
        image = Image.objects.filter(id=int(id)).first()
        
        if image:
            local_path = dir_path + '/' + image.name
            download_file(image.bucket, image.key, local_path)
    
    shutil.make_archive('tmp/images', 'zip', dir_path)
    
    wrapper = FileWrapper(open('tmp/images.zip', 'rb'))
    
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="images.zip"'
    
    return response


@csrf_exempt
def search(request):
    
    if request.method == 'GET' and request.GET.get('q'):
        template = get_template('images/snippets/image.html')
        
        images = Image.objects.filter(name__icontains=request.GET['q'])
        images = [template.render({'image': image}) for image in images]
        
        return JsonResponse({
            'success': True,
            'images': images,
        })