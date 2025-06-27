from django.urls import path
from . import views # Importa las vistas de tu misma aplicación

urlpatterns = [
     path('', views.home, name='home'), # La raíz apuntará a la vista de tu app el index
]