from django.urls import path
from .views import contacto_api, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
     #path('', views.home, name='home'),  La raíz apuntará a la vista de tu app el index
     path('contacto/', contacto_api, name='contacto_api'),

     path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
     path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),

]
