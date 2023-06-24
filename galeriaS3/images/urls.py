from django.urls import path

from .views import upload, update

app_name = 'images'

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('update/<int:pk>/', update, name='update'),
]