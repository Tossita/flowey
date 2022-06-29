#CORRESPONDE A LAS URLS QUE SE UTILIZARAN
from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)
router.register('user', MainUserViewSet)
router.register('tipo_producto', TipoProductoViewSet)
router.register('tipo_user', TipoUserViewSet)
router.register('suscripcion', SuscripcionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]