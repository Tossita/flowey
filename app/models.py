from xml.dom.minidom import CharacterData
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# Create your models here.
#Crear tablas sin declarar

class TipoProducto(models.Model):
    tipo = models.CharField(max_length=20)
    
    def __str__(self):
        return self.tipo
    
    class Meta:
        db_table='db_tipo_producto'

class Producto(models.Model):
    codigo = models.IntegerField(null=False, primary_key=True)
    nombre = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    stock = models.IntegerField()
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos", null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table='db_producto'

class TipoCliente(models.Model):
    tipo = models.CharField(max_length=20)
    
    def __str__(self):
        return self.tipo

    class Meta:
        db_table='db_tipo_cliente'

class Cliente(models.Model):
    run = models.CharField(max_length=13,null=False, primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    clave = models.CharField(max_length=20)
    correo = models.CharField(max_length=25)
    region = models.CharField(max_length=25)
    comuna = models.CharField(max_length=25)
    direccion = models.CharField(max_length=150)
    tipo = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="usuarios", null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.nombre

    class Meta:
        db_table='db_cliente'


class TipoUser(models.Model):
    tipo = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.tipo
    
    class Meta:
        db_table='db_tipo_user'


class MainUser(AbstractUser):

    tipo = models.ForeignKey(TipoUser, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.username


class Carrito (models.Model):
    cod_carr = models.AutoField(null=False, primary_key=True)
    comprado = models.BooleanField()
    total = models.IntegerField(null=True)
    descuento = models.IntegerField(null=True)
    subtotal = models.IntegerField(null=True)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)

    def __int__(self):
        return self.cod_carr

    class Meta:
        db_table='db_carrito'


class Seguimiento(models.Model):
    cod_seguimiento = models.AutoField(primary_key=True, null=False)
    estado = models.CharField(max_length=20)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __int__(self):
        return self.cod_seguimiento

    class Meta:
        db_table='db_seguimiento'



class ElementCarrito(models.Model):

    cod_element_carrito = models.AutoField(null=False, primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    comprado = models.BooleanField()

    def __int__(self):
        return self.cod_element_carrito

    class Meta:
        db_table='db_element_carrito'




class TipoPago(models.Model):
    tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.tipo

    class Meta:
        db_table='db_tipo_pago'



class Suscripcion(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    suscrito = models.BooleanField()

    def __boolean__(self):
        return self.suscrito

    class Meta:
        db_table='db_suscripcion'

class Historial(models.Model):
    num_hist = models.AutoField(primary_key=True, null = False)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE)

    def __int__(self):
        return self.num_carrito

    class Meta:
        db_table='db_historial'



#class Historial (models.Model):


