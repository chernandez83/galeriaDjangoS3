from django.urls import path
from .views import index

app_name = 'albums'

urlpatterns = [
    path('', index, name='list'),
]
