from django.urls import path

from .views import upload, update, show, delete, download, delete_many, download_many, search

app_name = 'images'

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('update/<int:pk>/', update, name='update'),
    path('show/<int:pk>/', show, name='show'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('download/<int:pk>/', download, name='download'),
    path('delete/many/', delete_many, name='delete_many'),
    path('download/many/', download_many, name='download_many'),
    path('search', search, name='search'),
]