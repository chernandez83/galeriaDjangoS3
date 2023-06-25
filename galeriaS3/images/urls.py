from django.urls import path

from .views import upload, update, show, delete

app_name = 'images'

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('update/<int:pk>/', update, name='update'),
    path('show/<int:pk>/', show, name='show'),
    path('delete/<int:pk>/', delete, name='delete'),
]