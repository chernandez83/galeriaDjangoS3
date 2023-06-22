from django.conf import settings

from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from .models import Album
from .forms import AlbumForm


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/detail.html'


class AlbumListView(ListView):
    model = Album
    template_name = 'albums/list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Galería'
        context['form'] = AlbumForm()

        return context


def create(request):
    form = AlbumForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        #album = form.save()
        album = Album.objects.create_by_aws(bucket=settings.BUCKET, title=form.cleaned_data['title'], description=form.cleaned_data['description'])

        return redirect('albums:list')
