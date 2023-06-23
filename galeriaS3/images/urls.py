from django.urls import path

from .views import upload

app_name = 'images'

urlpatterns = [
    path('upload/', upload, name='upload'),
]