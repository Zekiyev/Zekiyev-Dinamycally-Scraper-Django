from django.urls import path
from .views import upload_advertisements, upload_cities

urlpatterns = [
    #path('add_user/', upload_user, name='add_user'),
    path('add_adv/', upload_advertisements, name='add_adv'),
    path('add_cities',upload_cities, name='add_cities'),
]
