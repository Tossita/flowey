#SE ENCARGA DE HACER EL CRUD DESDE JSON

from app.models import *

from rest_framework import serializers

class TipoProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoSerializers(serializers.ModelSerializer):

    tipo = TipoProductoSerializers(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'

class TipoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUser
        fields = '__all__'

class MainUserSerializers(serializers.ModelSerializer):

    tipo = TipoUserSerializer(read_only=True)

    class Meta:
        model = MainUser
        fields = '__all__'

class SuscripcionSerializers(serializers.ModelSerializer):

    user = MainUserSerializers(read_only=True)

    class Meta:
        model = Suscripcion
        fields = '__all__'