from django.shortcuts import render

from .forms import AlbumForm

def index(request):
    form = AlbumForm()
    context = {
        'title': 'Galería',
        'form': form,
    }
    return render(request, 'albums/list.html', context)