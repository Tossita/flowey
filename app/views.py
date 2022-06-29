from ast import Global
from tkinter.tix import MAX
import requests #permite leer el api
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from distutils.log import debug
from itertools import count, product
from tracemalloc import stop
from.models import *
from.models import MainUser
from.forms import *
from app.forms import ProductoForm
from app.forms import ClienteForm
from django.db.models import Count
from django.contrib.auth.models import Group 





# Create your views here.




def index(request):
    return render(request, 'app/index.html')

@login_required
def perfil(request):
    num_visitas = request.session.get('num_visitas', 0)
    request.session['num_visitas'] = num_visitas + 1
    request.session.set_expiry(30)
    username = request.user.username
    datos = {'visitas' : num_visitas,
    'username' : username,}
    return render(request, 'app/perfil.html', datos)

@login_required
def indexU (request):
    usertest = MainUser.objects.get(id = request.user.id)
    if usertest.is_staff:
        print('asdasd')
        print(usertest.username)
        if usertest.tipo == None:
            print('aksdflasfdm')
            tipouser = TipoUser.objects.get(tipo = 'Administrador')
            
            usertest.tipo = tipouser
            usertest.save()
            
            
    else:
        print(usertest.username)
        print('asjdkfnasjnf')
        if usertest.tipo == None:
            print('44444')
            tipouser = TipoUser.objects.get(tipo = 'Cliente')
            
            usertest.tipo = tipouser
            usertest.save()
    print(usertest.tipo)

    if usertest.tipo == 'Cliente':
        usertest.permissions.add( "app.add_element_carrito", "app.view_producto", "app.delete_element_carrito", "app.change_element_carrito", "app.change_carrito" )



    return render(request, 'app/indexUsuario.html')

#def element_carrito (request):
   # return render(request, 'app/element_carritoCompras.html')
@permission_required('app.view_historial')
@login_required
def historial (request):
    historialAll = Historial.objects.filter(user = request.user)
    elementCarritoAll = ElementCarrito.objects.filter(user = request.user, comprado = True)
    


    print(historialAll)
    datos = {
        'listaElementCarrito' : elementCarritoAll,
        'listarHistorial' : historialAll,
    }

    return render(request, 'app/historial.html', datos)

def registro (request):
    datos = {
        'form' : ClienteForm()
    }
    if request.method == 'POST' :
        formulario = ClienteForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos ['mensaje'] = 'Cliente guardado correctamente!'

    return render(request, 'app/registro.html', datos)


#Seguimiento del usuario y del admin
@permission_required('app.view_seguimiento')
@login_required
def seguimiento (request):

    if request.method == 'GET':
        search = request.GET.get('search')
        seguimientos = []
        mostrar_seg = False
        seg_encontrado = False
        if search :
            try:
                seguimientos = Seguimiento.objects.get(user = request.user, cod_seguimiento=search)
                if seguimientos:
                    if seguimientos.estado == 'No comprado':
                        seg_encontrado = False
                    else:
                        seg_encontrado = True
                        
                else:
                    seg_encontrado = False
                mostrar_seg = True
            except:
                mostrar_seg = True
                seg_encontrado = False


            print('search')
    
    datos = {
        'mostrar_seg' : mostrar_seg,
        'seg_encontrado' : seg_encontrado,
        'seguimientos' : seguimientos,
    }
    

    return render(request, 'app/seguimiento.html', datos)

@permission_required('app.change_seguimiento')
@login_required
def seguimientoAdmin (request):

    seguimientoAll = Seguimiento.objects.all()

    

    datos = {
        'listarSeguimientos' : seguimientoAll,
    }



    return render(request, 'app/seguimientoAdmin.html',datos)


@login_required
def suscripcion (request):
    mensaje=''
    '''try:
        print('a')
        suscrito = Suscripcion.objects.get(user = request.user ) 
        suscrito_bool = True
    except:
        print('b')
        suscrito_bool = False'''
    suscrito = Suscripcion.objects.filter(user = request.user ) 
    if len(suscrito) == 0 :
        suscrito_bool = False
    else:
        suscrito_bool = True
    if request.method == 'POST' :
        print('ola')
        opcion = request.POST.get('suscrito')
        
        if opcion=='True' and len(suscrito) == 0:
            
            print('hola1')
            suscripcion=Suscripcion()
            suscripcion.user=request.user
            suscripcion.suscrito=True
            
            mensaje='Suscripción exitosa'
            suscripcion.save()
            suscrito_bool = True
            
        elif opcion=='False' and len(suscrito) != 0:
            print('hola2')
            suscripcion = Suscripcion.objects.get(user=request.user)
            suscripcion.delete()
            mensaje='Desuscripción exitosa'
            suscrito_bool = False


        elif len(suscrito) != 0:
            suscrito_bool = True

        else:
            suscrito_bool = False



    datos = {
        'dato' : mensaje,
        'suscrito_bool' : suscrito_bool
    }

    return render(request, 'app/suscripcion.html', datos)



@login_required
def usuario(request):
    productoAll = Producto.objects.all()
    datos = {
        'listaProductos' : productoAll
    }
    return render(request, 'app/usuario.html', datos)

@permission_required('app.view_user')
@login_required
def listar_usuarios(request):
    MainUserAll = MainUser.objects.all()
    datos = {
        'listarClientes' : MainUserAll
    }
    return render(request, 'app/listar_usuarios.html', datos)

#def usuario (request):
#   return render(request, 'app/usuario.html')

@login_required
def ventas (request):
    return render(request, 'app/ventas.html')

@permission_required('app.change_carrito')
@login_required
def compra_exitosa (request):
    
    element_carrito = ElementCarrito.objects.filter(user = request.user, comprado = False)
    
    #descuento stock
    '''for x in element_carrito:
        producto = Producto.objects.get(codigo=x.producto.codigo)
        producto.stock-=1
        producto.save()'''

    carrito = Carrito.objects.get(user = request.user,comprado = False)
    carrito.comprado = True
    carrito.save()

    seguimiento=Seguimiento.objects.get(carrito = carrito)

    seguimiento.estado = 'Validación'

    seguimiento.save()

    llenarHistorial(request.user, carrito, seguimiento)


    for x in element_carrito:
        x.comprado = True 
        x.save()

    datos = {
        'num_seg' : seguimiento.cod_seguimiento
    }
    
    
    return render(request, 'app/compra_exitosa.html', datos)

def base(request):
    return render(request, 'app/base.html')
   


def indexPrueba(request):
    return render(request, 'app/indexPrueba.html')

#elimnar
@permission_required('app.delete_producto')
@login_required
def eliminar_producto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    producto.delete()

    return redirect(to="listar_productos")

@permission_required('app.delete_user')
@login_required
def eliminar_usuarios(request, id):
    usuario = MainUser.objects.get(id=id)
    usuario.delete()

    return redirect(to="listar_usuarios")


def onprocess(request):
    return render(request, 'app/status_onprocess.html')


#seccion agregar
@permission_required('app.add_producto')
def agregar_producto(request):
    datos = {
        'form' : ProductoForm()
    }
    if request.method == 'POST' :
        formulario = ProductoForm(request.POST , files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto guardado correctamente!')
            

    return render(request, 'app/productos/agregar_producto.html', datos)
   

#seccion listar
@permission_required('app.view_producto')
@login_required
def ventasDos(request):
    
    if request.method == 'POST' :
        
        tipo = TipoProducto()
        tipo.tipo = request.POST.get('tipo')
        print(tipo.tipo)
        producto = Producto()
        producto.codigo = request.POST.get('codigo')
        producto.nombre = request.POST.get('nombre')
        producto.marca = request.POST.get('marca')
        producto.precio = request.POST.get('precio')
        producto.descripcion = request.POST.get('descripcion')
        producto.stock = request.POST.get('stock')
        producto.tipo = tipo
        producto.imagen = request.POST.get('imagen')
        carritos = Carrito.objects.filter(user = request.user, comprado= False)
 

        if len(carritos)== 0:
            carrito_new = Carrito()
            carrito_new.user = request.user
           
            carrito_new.comprado = False
            carrito_new.save()
            carrito = carrito_new
            seguimiento = Seguimiento()
            seguimiento.estado = 'No comprado'
            seguimiento.carrito = carrito_new
            seguimiento.user = request.user
            seguimiento.save()


        else:
            carrito = carritos[0]

        element_carritonuevo = ElementCarrito() 
        element_carritonuevo.user = request.user
        element_carritonuevo.producto = producto
        element_carritonuevo.cantidad = 0
        element_carritonuevo.comprado = False
        element_carritonuevo.carrito = carrito
        element_carritonuevo.save()

    #descuento stock
        if request.method == 'POST':
            producto = Producto.objects.get(codigo=producto.codigo)

            producto.stock-=1
            producto.save()
    response = requests.get('http://127.0.0.1:8000/api/producto/').json()
    productoAll = Producto.objects.all()
    datos = {
            'listaProductos' : productoAll,
            'listaJson': response
    }
    return render(request, 'app/ventasDos.html', datos)


@login_required
def ventas_api(request):
    response = requests.get('http://127.0.0.1:8000/api/producto/').json()
    response2 = requests.get('https://smashbros-unofficial-api.vercel.app/api/v1/ultimate/characters').json()
    response3 = requests.get('http://futuramaapi.herokuapp.com/api/v2/characters').json()
    productoAll = Producto.objects.all()
    datos = {
        'listaProductos' : productoAll,
        'listaJson': response,
        'listaSSB': response2 ,
        'listaF': response3 ,
    }
    if request.method == 'POST' :
        tipo = TipoProducto()
        tipo.tipo = request.POST.get('tipo')

        producto = Producto()
        producto.codigo = request.POST.get('codigo')
        producto.nombre = request.POST.get('nombre')
        producto.marca = request.POST.get('marca')
        producto.precio = request.POST.get('precio')
        producto.descripcion = request.POST.get('descripcion')
        producto.stock = request.POST.get('stock')
        producto.tipo = tipo
        producto.imagen = request.POST.get('imagen')

        element_carrito = ElementCarrito()
        element_carrito.producto = producto
        element_carrito.cantidad = 0
        element_carrito.save()



    return render(request, 'app/ventas_api.html', datos)



@login_required
def api_smash(request):
    
    response2 = requests.get('https://smashbros-unofficial-api.vercel.app/api/v1/ultimate/characters').json()
    response3 = requests.get('http://futuramaapi.herokuapp.com/api/v2/characters').json()
    datos = {

        'listaSSB': response2 ,
        'listaF': response3 ,
    }




    return render(request, 'app/api_smash.html', datos)



def base2(request):
    return render(request, 'app/base2.html')

#modificar
@permission_required('app.change_producto')
@login_required
def modificar_producto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    datos = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method == 'POST' :
        formulario = ProductoForm(request.POST, files=request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            datos ['mensaje'] = 'Producto modificado correctamente!'
            datos ['form'] = formulario

    return render(request, 'app/productos/modificar_producto.html', datos)

@permission_required('app.change_user')
@login_required
def modificar_usuarios(request, id):
    usuario = MainUser.objects.get(id=id)
    datos = {
        'form' : UserRegistroForm(instance=usuario)
    }
    if request.method == 'POST' :
        formulario = UserRegistroForm(request.POST, files=request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            datos ['mensaje'] = 'Usuario modificado correctamente!'
            datos ['form'] = formulario

    return render(request, 'app/modificar_usuarios.html', datos)

@permission_required('app.change_seguimiento')
@login_required
def modificar_seguimiento(request, cod_seguimiento):
    estados = ['No comprado','Validación', 'Preparación', 'Reparto', 'Entregado']
    seguimiento = Seguimiento.objects.get(cod_seguimiento=cod_seguimiento)
    
    if request.method == 'POST' :
        formulario = SeguimientoForm(request.POST, files=request.FILES, instance=seguimiento)
        estado = request.POST.get('estado')
        seguimiento.estado = estado
        seguimiento.save()

    datos = {
        'form' : SeguimientoForm(instance=seguimiento),
        'seguimiento' : seguimiento,
        'estados' : estados

    }



    return render(request, 'app/modificar_seguimiento.html', datos)


#listar
@permission_required('app.view_producto')
@login_required
def listar_productos(request):
    productoAll = Producto.objects.all()
    datos = {
        'listarProductos' : productoAll
    }

    
    return render(request, 'app/productos/listar_productos.html', datos)

@permission_required('app.change_producto')
def modificar_producto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    datos = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method == 'POST' :
        formulario = ProductoForm(request.POST, files=request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            datos ['mensaje'] = 'Producto modificado correctamente!'
            datos ['form'] = formulario

    return render(request, 'app/productos/modificar_producto.html', datos)


@permission_required('app.change_carrito', 'app.add_carrito')
@login_required
def carritoCompras(request):
    if request.method == 'POST' :
        sacarProducto = request.POST.get('sacarProducto')
        codigoProducto = request.POST.get('prod')
        
        prod=Producto.objects.get(codigo = codigoProducto)

        borrar_elemente = ElementCarrito.objects.filter(producto=prod, user = request.user, comprado = False )
        borrar_elemente[0].delete()
        
        producto = Producto.objects.get(codigo=prod.codigo)
        producto.stock+=1
        producto.save()

    element_carrito = ElementCarrito.objects.filter(user = request.user, comprado = False )

    listaElementCarrito = []
    listaCodigo = []
    total = 0
    subtotal=0
    descuento =0
    

    for x in element_carrito:
        
    	if x.producto.codigo not in listaCodigo:
            listaElementCarrito.append(x)
            listaCodigo.append(x.producto.codigo)

    for x in listaElementCarrito:
        for y in element_carrito:
            if x.producto.codigo == y.producto.codigo:
                x.cantidad += 1

    for x in listaElementCarrito:
        cantidad_pro = x.cantidad
        precio_pro = x.producto.precio
        total_por_producto = cantidad_pro*precio_pro
        subtotal+=total_por_producto
    descuento = 0
    try:
        suscripcion = Suscripcion.objects.get(user=request.user)

        if suscripcion.suscrito :
            descuento = round(subtotal*0.05)
        else:
            descuento = 0
    except:
        descuento = 0

    
    total = subtotal-descuento

    try:
        carrito = Carrito.objects.get(cod_carr = element_carrito[0].carrito.cod_carr)
        carrito.total = total
        carrito.descuento = descuento
        carrito.subtotal = subtotal
        carrito.save()
    except:
        pass
    datos = {
        'listaElementCarrito' : listaElementCarrito,

        'subtotal': subtotal,
        'descuento': descuento,
        'total': total,
    }

    

    


    

    return render(request, 'app/carritoCompras.html', datos)


def registro_usuarios(request):
    try:
        Group.objects.create(name="Administrador")
        administrador = Group.objects.get(name="Administrador")
        Group.objects.create(name="Cliente")
        cliente = Group.objects.get(name="Cliente")
    except:
        pass
    



    datos = {
        'form' : UserRegistroForm()
    }
    print('hola')
    if request.method == 'POST':
        formulario = UserRegistroForm(data=request.POST)
        #mainuser = MainUser()
        #tipouser = TipoUser.objects.get(tipo ='Cliente')
        #user = User.objects.get(tipo ='Cliente')
        
        
        if formulario.is_valid():
            formulario.save()
            usergroup = MainUser.objects.get(id = formulario.instance.id)
            my_group = Group.objects.get(name='Cliente') 
            my_group.user_set.add(usergroup)
            tipouser = TipoUser.objects.get(tipo = 'Cliente')
            messages.success(request,'Registrado correctamente!')
            usergroup.tipo = tipouser
            usergroup.save()
            my_group.save()

            datos["form"] = formulario
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            
            return redirect(to="index")
        
    return render(request, 'registration/registro_usuarios.html', datos)



    





def llenarHistorial(user, carrito, seguimiento):
    historial = Historial()
    historial.user = user
    historial.carrito = carrito
    historial.seguimiento = seguimiento
    historial.save()

@permission_required('app.view_historial')
def historial_detallado(request, num_hist):
    historial = Historial.objects.get(num_hist=num_hist)
    listaElementoCarr = ElementCarrito.objects.raw('SELECT *, COUNT(producto_id) as "contador" FROM db_element_carrito WHERE carrito_id = %s GROUP BY producto_id', [historial.carrito_id])
    for x in listaElementoCarr:
        print(x.contador)
        a = x
    #filter(carrito = historial.carrito).annotate(count=Count('producto'))


    datos = {
        'carrito' : historial.carrito,
        'seguimiento' : historial.seguimiento,
        'listaElementos' : listaElementoCarr,
    }
    

    return render(request, 'app/historial_detallado.html', datos)



