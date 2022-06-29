from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from app.models import *

# Create your views here.


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializers

class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializers

class MainUserViewSet(viewsets.ModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = MainUserSerializers

class TipoUserViewSet(viewsets.ModelViewSet):
    queryset = TipoUser.objects.all()
    serializer_class = TipoUserSerializer

class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = Suscripcion.objects.all()
    serializer_class = SuscripcionSerializers

