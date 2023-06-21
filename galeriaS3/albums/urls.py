from django.urls import path
from .views import create, AlbumDetailView, AlbumListView

app_name = 'albums'

urlpatterns = [
    path('', AlbumListView.as_view(), name='list'),
    path('create', create, name='create'),
    path('<int:pk>/detail', AlbumDetailView.as_view(), name='detail'),
]
