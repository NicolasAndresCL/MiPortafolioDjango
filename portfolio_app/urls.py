from django.urls import path
from .views import contacto_api

urlpatterns = [
     #path('', views.home, name='home'),  La raíz apuntará a la vista de tu app el index
     path('contacto/', contacto_api, name='contacto_api')
]
