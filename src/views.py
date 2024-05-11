from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django import forms
from src.forms import (
    FormCliente, FormProveedor, FormProducto,
    FormProveedorAct, FormFamiliaProd, FormProductoProv, 
    FormProductoEdit, FormClientesParaVenta, 
    FormCategProv, FormTipoProducto)
from datetime import datetime
import re
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage




def Login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == 'POST':
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.warning(request, 'Usuario o contraseña incorrectos')

    return render(request, 'registration/login.html')

@login_required(login_url="login")
def Index(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    return render(request, 'index.html')

@login_required(login_url="login")
def Venta(request):

    usuarioBoleta = request.user
    usuarioBoleta = User.objects.get(username=usuarioBoleta)

    productos = PRODUCTO.objects.all()
    form = FormClientesParaVenta()
    admin = User.objects.filter(username='Sra.Juanita')

    for juanita in admin:
        admin = juanita

    total = 0
    cliente = 0
    listaProductos = []
    cont = 0

    if request.method == 'POST':

        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        queryCliente = request.POST.get('cliente')
        fecha_pago = request.POST.get('fecha_pago')

        if queryCliente != '':

            if usuario == "admin":

                user = authenticate(request, username = usuario, password = contrasena)
                
                if user is not None:
                    contador = 0
                    for key,value in request.POST.items():
                        contador = contador + 1

                    contador2 = 0
                    producto = []
                    for key,value in request.POST.items():

                        contador2 = contador2 + 1

                        if contador2 == contador:

                            total = value

                        if contador2 > 1 and contador2 < contador - 2:

                            if key == 'cliente':
                                cliente = value

                            if contador2 > 3:
                                cont += 1

                                producto.append(value)
                                
                                if cont == 3:
                                    listaProductos.append(producto)
                                    producto = []
                                    cont = 0

                    cliente = CLIENTE.objects.filter(id=cliente)
                    for client in cliente:
                        cliente = client

                    boleta = BOLETA.objects.create(
                        total_a_pagar = total,
                        usuario = usuarioBoleta,
                        cliente = cliente,
                        estado = 1
                    )
                    boleta.save()

                    bol = BOLETA.objects.all().last()
                    bol = BOLETA.objects.get(id = bol.id)
                    
                    for listaP in listaProductos:
                        
                        prod = PRODUCTO.objects.get(codigo_barra = listaP[0])
                        
                        detalleBoleta = DETALLE_BOLETA.objects.create(
                            boleta = bol,
                            cantidad = listaP[1],
                            monto_a_pagar = listaP[2],
                            producto = prod
                        )
                        detalleBoleta.save()
                    
                    fecha_pago = fecha_pago[6:10] + '-' + fecha_pago[3:5] + '-' + fecha_pago[0:2]
                    pago_fiado = PAGO_FIADO.objects.create(
                        estado = 1,
                        monto = total,
                        fecha_final = fecha_pago,
                        cliente = CLIENTE.objects.get(id=queryCliente) 
                    )

                    pago_fiado.save()
                    
                    messages.warning(request, 'Fiado realizado')
                    return redirect('venta')

                else:
                    messages.warning(request, 'Usuario o contraseña incorrectos')
            else:
                messages.warning(request, 'Usuario ingresado no es administrador')

        else:
            if request.method == 'POST':
                usuarioBoleta = request.user
                usuarioBoleta = User.objects.get(username=usuarioBoleta)
                contador = 0

                for key,value in request.POST.items():
                    contador = contador + 1

                contador2 = 0
                producto = []
                for key,value in request.POST.items():
                    
                    contador2 = contador2 + 1

                    if contador2 == contador:

                        total = value

                    if contador2 > 1 and contador2 < contador:
                        
                        if contador2 > 3:
                            cont += 1
                            
                            producto.append(value)

                            if cont == 3:
                                listaProductos.append(producto)
                                producto = []
                                cont = 0

                boleta = BOLETA.objects.create(
                    total_a_pagar = total,
                    usuario = usuarioBoleta,
                    estado = 1
                )
                boleta.save()

                bol = BOLETA.objects.all().last()
                bol = BOLETA.objects.get(id = bol.id)

                for listaP in listaProductos:
                    prod = PRODUCTO.objects.get(codigo_barra = listaP[0])
                    
                    detalleBoleta = DETALLE_BOLETA.objects.create(
                        boleta = bol,
                        cantidad = listaP[1],
                        monto_a_pagar = listaP[2],
                        producto = prod
                    )
                    detalleBoleta.save()

                messages.warning(request, 'Venta realizada con exito')
                return redirect('venta')

    return render(request, 'venta.html',{'productos':productos, 'form':form})

@login_required(login_url="login")
def RecepcionPedido(request, id = None):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    ordenPedido = ORDEN_PEDIDO.objects.all()
    detalleOrden = DETALLE_ORDEN.objects.all()
    productos = ""
    ordenPedido2 = ""
    detalleOrden2 = ""
    if id:
        ordenPedido2 = ORDEN_PEDIDO.objects.filter(id=id)
        detalleOrden2 = DETALLE_ORDEN.objects.filter(orden_pedido=id)
        productos = PRODUCTO.objects.all()

    if request.method == 'POST':

        ordenPedido3 = ORDEN_PEDIDO.objects.get(id=id)
        fecha = datetime.now().date()
        hora = datetime.now().time()
        print(fecha)
        print(hora)

        ordenPedido3.estado_recepcion = 1
        ordenPedido3.save()
        ordenPedido3.fecha_recepcion = fecha
        ordenPedido3.save()
        ordenPedido3.hora_recepcion = hora
        ordenPedido3.save()

        return redirect('RecepcionPedido')

    context= {
        'ordenPedido':ordenPedido,
        'productos':productos,
        'detalleOrden':detalleOrden,
        'ordenPedido2':ordenPedido2,
        'detalleOrden2':detalleOrden2
    }
    return render(request, 'recepcion_pedido.html',context)

@login_required(login_url="login")
def ClienteListado(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    clientes = CLIENTE.objects.all()

    return render(request, 'clientes/listar.html', {'clientes':clientes})

@login_required(login_url="login")
def ClienteCrear(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    run = request.POST.get('run')
    nombre = request.POST.get('nombre')
    telefono = request.POST.get('telefono')
    correo = request.POST.get('correo')
    direccion = request.POST.get('direccion')
    validarRun = CLIENTE.objects.filter(run=run)

    if request.method == 'POST':
        if validarRun:
            messages.warning(request, 'el run ya existe')
        else:
            if (ValidacionCamposCliente(request,
                run, nombre, telefono, correo, direccion)
            ):
                cliente = CLIENTE.objects.create(
                    run = run.strip(),
                    nombre = nombre.strip(),
                    telefono = telefono.strip(),
                    correo = correo.strip(),
                    direccion = direccion.strip(),
                    estado = 1
                )

                if cliente is not None:
                    cliente.save()
                    messages.warning(request, 'Cliente creado correctamente')
                    return redirect('listarClientes')
                else:
                    messages.warning(request, 'No se pudo crear el cliente')
            else:
                messages.warning(request, 'No se pudo crear el cliente')

    return render(request, 'clientes/crear.html')

@login_required(login_url="login")
def ClienteActualizar(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    cliente = CLIENTE.objects.get(id=id)
    form = FormCliente(request.POST or None, instance=cliente)

    run = request.POST.get('run')
    nombre = request.POST.get('nombre')
    telefono = request.POST.get('telefono')
    correo = request.POST.get('correo')
    direccion = request.POST.get('direccion')

    if request.method == 'POST':
        if (ValidacionCamposCliente(request,
            run, nombre, telefono, correo, direccion)
        ):
            if cliente is not None:

                cliente.run = run.strip()
                cliente.save()
                cliente.nombre = nombre.strip()
                cliente.save()
                cliente.telefono = telefono.strip()
                cliente.save()
                cliente.correo = correo.strip()
                cliente.save()
                cliente.direccion = direccion.strip()
                cliente.save()
                messages.warning(request, 'Cliente actualizado correctamente')
                return redirect('listarClientes')
            else:
                messages.warning(request, 'No se pudo actualizar el cliente')
        else:
            messages.warning(request, 'No se pudo actualizar el cliente')

    return render(request, 'clientes/actualizar.html', {'form':form})

def ValidacionCamposCliente(request, run, nombre, telefono, correo, direccion):

    estado = False
    run.strip()
    nombre.strip()
    telefono.strip()
    correo.strip()
    direccion.strip()

    if len(run) < 7:
        messages.warning(request, 'La cantidad de caracteres del run debe ser mayor a 6')
    elif len(run) > 10:
        messages.warning(request, 'La cantidad de caracteres del run debe ser menor a 11')
    elif len(nombre) < 3:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser mayor a 2')
    elif len(nombre) > 100:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser menor a 101')
    elif len(telefono) < 5:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser mayor a 4')
    elif len(telefono) > 12:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser menor a 13')
    elif len(correo) < 5:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser mayor a 4')
    elif len(correo) > 128:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser menor a 129')
    elif len(direccion) < 3:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser mayor a 2')
    elif len(direccion) > 150:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser menor a 151')
    else:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
            estado = True
        else:
            messages.warning(request, 'El correo no cumple con la estructura basica')

    return estado

@login_required(login_url="login")
def ClienteDetalle(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    cliente = CLIENTE.objects.get(id=id)
    return render(request, 'clientes/detalles.html', {'cliente':cliente})

def DesactivarCliente(request, id):
    cliente = CLIENTE.objects.get(id = id)
    cliente.estado = 0
    cliente.save()
    messages.warning(request, f'Cliente {cliente.nombre} desactivado')
    return redirect('listarClientes')

def ActivarCliente(request, id):
    cliente = CLIENTE.objects.get(id = id)
    cliente.estado = 1
    cliente.save()
    messages.warning(request, f'Cliente {cliente.nombre} activado')
    return redirect('listarClientes')

@login_required(login_url="login")
def ProveedorListado(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)
    proveedores = PROVEEDOR.objects.all()

    return render(request, 'proveedores/listar.html', {'proveedores':proveedores})

@login_required(login_url="login")
def ProveedorCrear(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    form = FormProveedor(request.POST)
    razon_social = request.POST.get('razon_social')
    correo = request.POST.get('correo')
    telefono = request.POST.get('telefono')
    direccion = request.POST.get('direccion')
    categoria = request.POST.get('categoria_proveedor')
    categoria = CATEGORIA_PROVEEDOR.objects.filter(id = categoria)
    for cat in categoria:
        categoria = cat

    if request.method == 'POST':

        if (ValidacionCamposProveedor(request,
            razon_social, correo, telefono, direccion)
        ):
            proveedor = PROVEEDOR.objects.create(
                razon_social = razon_social.strip(),
                correo = correo.strip(),
                telefono = telefono.strip(),
                direccion = direccion.strip(),
                categoria_proveedor = categoria,
                estado = 1
            )

            if proveedor is not None:
                proveedor.save()
                messages.warning(request, 'Proveedor creado correctamente')
                return redirect('listarProveedores')
            else:
                messages.warning(request, 'No se pudo crear el Proveedor')

    return render(request, 'proveedores/crear.html',{'form':form})

@login_required(login_url="login")
def ProveedorActualizar(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    proveedor = PROVEEDOR.objects.get(id=id)
    form = FormProveedorAct(request.POST or None, instance=proveedor)
    razon_social = request.POST.get('razon_social')
    correo = request.POST.get('correo')
    telefono = request.POST.get('telefono')
    direccion = request.POST.get('direccion')

    categoria = request.POST.get('categoria_proveedor')
    categoria = CATEGORIA_PROVEEDOR.objects.filter(id = categoria)
    for cat in categoria:
        categoria = cat

    if request.method == 'POST':
        if (ValidacionCamposProveedor(request,
            razon_social, correo, telefono, direccion)
        ):
            if proveedor is not None:

                proveedor.razon_social = razon_social.strip()
                proveedor.save()
                proveedor.correo = correo.strip()
                proveedor.save()
                proveedor.telefono = telefono.strip()
                proveedor.save()
                proveedor.direccion = direccion.strip()
                proveedor.save()
                proveedor.categoria_proveedor = categoria
                proveedor.save()

                messages.warning(request, 'Proveedor actualizado correctamente')
                return redirect('listarProveedores')
            else:
                messages.warning(request, 'No se pudo actualizar el proveedor')
        else:
            messages.warning(request, 'No se pudo actualizar el proveedor')

    return render(request, 'proveedores/actualizar.html', {'form':form})

def ValidacionCamposProveedor(request, razon_social, correo, telefono, direccion):
    estado = False
    razon_social.strip()
    correo.strip()
    telefono.strip()
    direccion.strip()

    if len(razon_social) < 3:
        messages.warning(request, 'La cantidad de caracteres de la razon social debe ser mayor a 2')
    elif len(razon_social) > 100:
        messages.warning(request, 'La cantidad de caracteres de la razon social debe ser menor a 11')
    elif len(correo) < 3:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser mayor a 2')
    elif len(correo) > 100:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser menor a 101')
    elif len(telefono) < 5:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser mayor a 4')
    elif len(telefono) > 12:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser menor a 13')
    elif len(direccion) < 3:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser mayor a 2')
    elif len(direccion) > 150:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser menor a 151')
    else:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
            estado = True
        else:
            messages.warning(request, 'El correo no cumple con la estructura basica')

    return estado

@login_required(login_url="login")
def ProveedorDetalle(request, id):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)
    proveedor = PROVEEDOR.objects.get(id=id)

    return render(request, 'proveedores/detalles.html', {'proveedor':proveedor})

def DesactivarProveedor(request, id):
    proveedor = PROVEEDOR.objects.get(id = id)
    proveedor.estado = 0
    proveedor.save()
    messages.warning(request, f'Proveedor {proveedor.razon_social} desactivado')

    return redirect('listarProveedores')

def ActivarProveedor(request, id):
    proveedor = PROVEEDOR.objects.get(id = id)
    proveedor.estado = 1
    proveedor.save()
    messages.warning(request, f'Cliente {proveedor.razon_social} activado')

    return redirect('listarProveedores')

@login_required(login_url="login")
def ProductoListado(request):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)
    productos = PRODUCTO.objects.all()
    
    return render(request, 'productos/listar.html', {'productos':productos})

@login_required(login_url="login")
def ProductoCrear(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    formProd = FormProducto(request.POST)
    formFam = FormFamiliaProd(request.POST)
    formProv = FormProductoProv(request.POST)
    nombre = request.POST.get('nombre')
    precio = request.POST.get('precio')
    precio_compra = request.POST.get('precio_compra')
    descripcion = request.POST.get('descripcion')
    stock = request.POST.get('stock')
    stock_critico = request.POST.get('stock_critico')
    proveedor = request.POST.get('proveedor')
    familia_producto = request.POST.get('familia_producto')
    fecha_vencimiento = request.POST.get('fecha_vencimiento')
    hora_vencimiento = request.POST.get('hora_vencimiento')
    tipo_producto = request.POST.get('tipo_producto')

    if request.method == 'POST':

        if (ValidacionCamposProducto(request,
            nombre, precio, descripcion, precio_compra, stock, stock_critico, proveedor, familia_producto, tipo_producto)
        ):
            if fecha_vencimiento:
                fecha_v = fecha_vencimiento[6:10] + '-' + fecha_vencimiento[3:5] + '-' + fecha_vencimiento[0:2] + ' ' + hora_vencimiento + ':00'
                fecha_vencimiento = fecha_vencimiento[0:2]+fecha_vencimiento[3:5]+fecha_vencimiento[6:10]
            else:
                fecha_v = "1000-10-10 00:00:00"
                fecha_vencimiento = "00000000"

            familia_producto = str(familia_producto).zfill(3)
            tipo_producto = str(tipo_producto).zfill(3)
            proveedor = str(proveedor).zfill(3)

            codigo_barra = proveedor + familia_producto + fecha_vencimiento + tipo_producto

            if familia_producto:
                familia_producto = FAMILIA_PRODUCTO.objects.filter(id = familia_producto)
            for famP in familia_producto:
                familia_producto = famP

            producto = PRODUCTO.objects.create(
                nombre = nombre.strip(),
                precio = precio.strip(),
                descripcion = descripcion.strip(),
                precio_compra = precio_compra.strip(),
                stock = stock.strip(),
                stock_critico = stock_critico.strip(),
                estado = 1,
                fecha_vencimiento = fecha_v,
                codigo_barra = codigo_barra,
                familia_producto = familia_producto
            )

            if producto is not None:
                producto.save()
                messages.warning(request, 'Producto creado correctamente')
                return redirect('listarProductos')
            else:
                messages.warning(request, 'No se pudo crear el Producto')

    return render(request, 'productos/crear.html',{'formProd':formProd, 'formFam':formFam, 'formProv':formProv})

@login_required(login_url="login")
def ProductoActualizar(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    producto = PRODUCTO.objects.get(id=id)

    form = FormProductoEdit(request.POST or None, instance=producto)
    formProd = FormProducto(request.POST or None, instance=producto)

    tipo_producto = len(producto.codigo_barra)
    tipo_producto = int(producto.codigo_barra[-3:tipo_producto])
    tipo_producto = TIPO_PRODUCTO.objects.get(id=tipo_producto)

    proveedor = int(producto.codigo_barra[0:3])
    proveedor = PROVEEDOR.objects.get(id=proveedor)

    fecha = str(producto.fecha_vencimiento)
    hora = str(producto.fecha_vencimiento)
    fecha = fecha[0:10]
    hora = hora[11:16]

    formFam = FormFamiliaProd(request.POST or None, instance=tipo_producto)
    formProv = FormProductoProv(request.POST or None, instance=proveedor)

    context = {
        'formProd':formProd,
        'formFam':formFam,
        'formProv':formProv,
        'form':form,
        'tipo_producto':tipo_producto,
        'proveedor':proveedor,
        'fecha':fecha,
        'hora':hora
    }

    nombre = request.POST.get('nombre')
    precio = request.POST.get('precio')
    precio_compra = request.POST.get('precio_compra')
    descripcion = request.POST.get('descripcion')
    stock = request.POST.get('stock')
    stock_critico = request.POST.get('stock_critico')
    proveedor = request.POST.get('proveedor')
    familia_producto = request.POST.get('familia_producto')
    fecha_vencimiento = request.POST.get('fecha_vencimiento')
    hora_vencimiento = request.POST.get('hora_vencimiento')
    tipo_producto = request.POST.get('tipo_producto')

    if request.method == 'POST':
        if (ValidacionCamposProducto(request,
                nombre, precio, descripcion, precio_compra, stock, stock_critico, proveedor, familia_producto, tipo_producto)
            ):
                if fecha_vencimiento:
                    fecha_v = fecha_vencimiento[6:10] + '-' + fecha_vencimiento[3:5] + '-' + fecha_vencimiento[0:2] + ' ' + hora_vencimiento + ':00'
                    fecha_vencimiento = fecha_vencimiento[0:2]+fecha_vencimiento[3:5]+fecha_vencimiento[6:10]
                else:
                    fecha_v = "1000-10-10 00:00:00"
                    fecha_vencimiento = "00000000"

                familia_producto = str(familia_producto).zfill(3)
                tipo_producto = str(tipo_producto).zfill(3)
                proveedor = str(proveedor).zfill(3)

                codigo_barra = proveedor + familia_producto + fecha_vencimiento + tipo_producto

                if familia_producto:
                    familia_producto = FAMILIA_PRODUCTO.objects.filter(id = familia_producto)
                for famP in familia_producto:
                    familia_producto = famP

                if producto is not None:
                    producto.nombre = nombre.strip()
                    producto.save()

                    producto.precio = precio.strip()
                    producto.save()

                    producto.descripcion = descripcion.strip()
                    producto.save()

                    producto.precio_compra = precio_compra.strip()
                    producto.save()
                    producto.stock = stock.strip()
                    producto.save()
                    producto.stock_critico = stock_critico.strip()
                    producto.save()
                    producto.estado = 1
                    producto.save()
                    producto.fecha_vencimiento = fecha_v
                    producto.save()
                    producto.codigo_barra = codigo_barra
                    producto.save()
                    producto.familia_producto = familia_producto
                    producto.save()

                    messages.warning(request, 'Producto actualizado correctamente')
                    return redirect('listarProductos')
                else:
                    messages.warning(request, 'No se pudo actualizar el Producto')

    return render(request, 'productos/actualizar.html',context)

def ValidacionCamposProducto(request,nombre,precio,descripcion,precio_compra,stock,stock_critico,proveedor,familia_producto,tipo_producto):
    estado = False
    nombre.strip()
    precio.strip()
    descripcion.strip()
    precio_compra.strip()
    stock.strip()
    stock_critico.strip()

    if len(nombre) < 3:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser mayor a 2')
    elif len(nombre) > 100:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser menor a 101')
    elif len(precio) < 1:
        messages.warning(request, 'La cantidad de caracteres del precio debe ser mayor a 0')
    elif len(precio) > 10:
        messages.warning(request, 'La cantidad de caracteres del precio debe ser menor a 11')
    elif len(descripcion) < 4:
        messages.warning(request, 'La cantidad de caracteres de la descripcion debe ser mayor a 3')
    elif len(descripcion) > 200:
        messages.warning(request, 'La cantidad de caracteres de la descripcion debe ser menor a 201')
    elif len(precio_compra) < 1:
        messages.warning(request, 'La cantidad de caracteres del precio de compra debe ser mayor a 0')
    elif len(precio_compra) > 10:
        messages.warning(request, 'La cantidad de caracteres del precio de compra debe ser menor a 11')
    elif len(stock) < 1:
        messages.warning(request, 'La cantidad de caracteres del stock debe ser mayor a 0')
    elif len(stock) > 10:
        messages.warning(request, 'La cantidad de caracteres del stock debe ser menor a 11')
    elif len(stock_critico) < 1:
        messages.warning(request, 'La cantidad de caracteres del stock critico debe ser mayor a 0')
    elif len(stock_critico) > 10:
        messages.warning(request, 'La cantidad de caracteres del stock critico debe ser menor a 11')
    elif len(proveedor) == 0:
        messages.warning(request, 'Se debe seleccionar al menos una opcion en proveedor')
    elif len(familia_producto) == 0:
        messages.warning(request, 'Se debe seleccionar al menos una opcion en familia de producto')
    elif len(tipo_producto) == 0:
         messages.warning(request, 'Se debe seleccionar al menos una opcion en tipo de producto')
    else:
        estado = True

    return estado

@login_required(login_url="login")
def ProductoDetalle(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)
    producto = PRODUCTO.objects.get(id=id)

    return render(request, 'productos/detalles.html', {'producto':producto})

def DesactivarProducto(request, id):
    producto = PRODUCTO.objects.get(id = id)
    producto.estado = 0
    producto.save()
    messages.warning(request, f'Producto {producto.nombre} desactivado')

    return redirect('listarProductos')

def ActivarProducto(request, id):
    producto = PRODUCTO.objects.get(id = id)
    producto.estado = 1
    producto.save()
    messages.warning(request, f'Producto {producto.nombre} activado')

    return redirect('listarProductos')

@login_required(login_url="login")
def TipoProductoListado(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    tipos = TIPO_PRODUCTO.objects.all()

    return render(request, 'tipos_productos/listar.html', {'tipos':tipos})

@login_required(login_url="login")
def TipoProductoCrear(request):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    form = FormTipoProducto()

    if request.method == 'POST':

        descripcion = request.POST.get('descripcion')
        proveedor = request.POST.get('proveedor')
        
        if len(descripcion) <= 3:
            messages.warning(request, 'La descripcion no puede tener una cantidad de caracteres menor a 3')
        elif proveedor == "":
            messages.warning(request, 'En proveedor debe seleccionar alguno de la lista')
        else:
            proveedor = PROVEEDOR.objects.get(id = proveedor)

            tipo_producto = TIPO_PRODUCTO.objects.create(
                descripcion = descripcion,
                proveedor = proveedor,
            )

            if tipo_producto is not None:
                tipo_producto.save()
                messages.warning(request, 'Tipo producto creado correctamente')
                return redirect('listarTiposProductos')
            else:
                messages.warning(request, 'No se pudo crear el tipo producto')

    return render(request, 'tipos_productos/crear.html',{'form':form})

@login_required(login_url="login")
def TipoProductoActualizar(request, id):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)


    tipo_producto = TIPO_PRODUCTO.objects.get(id=id)
    form = FormTipoProducto(request.POST or None, instance=tipo_producto)
    
    if request.method == 'POST':

        descripcion = request.POST.get('descripcion')
        proveedor = request.POST.get('proveedor')

        if len(descripcion) <= 3:
            messages.warning(request, 'La descripcion no puede tener una cantidad de caracteres menor a 3')
        elif proveedor == "":
            messages.warning(request, 'En proveedor debe seleccionar alguno de la lista')
        elif tipo_producto is not None:
            proveedor = PROVEEDOR.objects.get(id = proveedor)
            tipo_producto.descripcion = descripcion
            tipo_producto.save()
            tipo_producto.proveedor = proveedor
            tipo_producto.save()

            messages.warning(request, 'Tipo producto actualizado correctamente')
            return redirect('listarTiposProductos')
        else:
            messages.warning(request, 'No se pudo actualizar el tipo producto')
        
    return render(request, 'tipos_productos/actualizar.html',{'form':form})

@login_required(login_url="login")
def FamiliaProductoListado(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    familiaP = FAMILIA_PRODUCTO.objects.all()
    return render(request, 'familia_producto/listar.html', {'familiaP':familiaP})

@login_required(login_url="login")
def FamiliaProductoCrear(request):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    form = FormFamiliaProd()

    if request.method == 'POST':

        descripcion = request.POST.get('descripcion')
        tipo_producto = request.POST.get('tipo_producto')
        
        if len(descripcion) <= 3:
            messages.warning(request, 'La descripcion no puede tener una cantidad de caracteres menor a 3')
        elif tipo_producto == "":
            messages.warning(request, 'En tipo producto debe seleccionar alguno de la lista')
        else:
            tipo_producto = TIPO_PRODUCTO.objects.get(id = tipo_producto)
            
            familia_producto = FAMILIA_PRODUCTO.objects.create(
                descripcion = descripcion,
                tipo_producto = tipo_producto,
            )

            if familia_producto is not None:
                familia_producto.save()
                messages.warning(request, 'Familia producto creado correctamente')
                return redirect('listarFamiliasProductos')
            else:
                messages.warning(request, 'No se pudo crear el familia producto')

    return render(request, 'familia_producto/crear.html',{'form':form})
   
@login_required(login_url="login")
def FamiliaProductoActualizar(request, id):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    familia_producto = FAMILIA_PRODUCTO.objects.get(id=id)
    form = FormFamiliaProd(request.POST or None, instance=familia_producto)
    
    if request.method == 'POST':

        descripcion = request.POST.get('descripcion')
        tipo_producto = request.POST.get('tipo_producto')

        if len(descripcion) <= 3:
            messages.warning(request, 'La descripcion no puede tener una cantidad de caracteres menor a 3')
        elif tipo_producto == "":
            messages.warning(request, 'En proveedor debe seleccionar alguno de la lista')
        elif familia_producto is not None:
            tipo_producto = TIPO_PRODUCTO.objects.get(id = tipo_producto)

            familia_producto.descripcion = descripcion
            familia_producto.save()
            familia_producto.tipo_producto = tipo_producto
            familia_producto.save()

            messages.warning(request, 'Familia producto actualizado correctamente')
            return redirect('listarFamiliasProductos')
        else:
            messages.warning(request, 'No se pudo actualizar la familia producto')
        
    return render(request, 'familia_producto/actualizar.html',{'form':form})

@login_required(login_url="login")
def PedidosListado(request):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    ordenP = ORDEN_PEDIDO.objects.all()
    return render(request, 'pedidos/listar.html', {'ordenP':ordenP})

def PedidosCrear(request, id = None):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    proveedores = PROVEEDOR.objects.all()
    tiposProductos = TIPO_PRODUCTO.objects.filter(proveedor=id)

    listaF = []
    for tiposP in tiposProductos:
        famId = FAMILIA_PRODUCTO.objects.filter(tipo_producto=tiposP)
        for f in famId:
            listaF.append(f.id)

    productos = PRODUCTO.objects.all()

    listaProds = []
    for prod in productos:
        idFam = FAMILIA_PRODUCTO.objects.filter(descripcion=prod.familia_producto)

        for idF in idFam:

            for listF in listaF:
                if listF == idF.id:

                    listaProds.append(prod.nombre)

    if request.method == 'POST':

        listaProductos = []
        producto = []

        contador2 = 0
        for key,value in request.POST.items():
            contador2 += 1

        contador = 0
        fecha = ""
        cont = 0
        for key,value in request.POST.items():
            
            contador += 1
            if contador == 2:
                proveedorOrden = int(value)

            if contador > 2:

                if contador == contador2:
                    if value == "":
                        fecha = "1000-10-10"
                    else:
                        fecha = value
                        fecha = fecha[6:10]+ '-' +fecha[3:5]+ '-' + fecha[0:2]
                        print(fecha)

                if contador < contador2:
                    cont += 1

                    producto.append(value)

                    if cont == 2:
                        listaProductos.append(producto)
                        producto = []
                        cont = 0

        proveedorOrden = PROVEEDOR.objects.get(id=proveedorOrden)

        ordenPedido = ORDEN_PEDIDO.objects.create(
            estado_recepcion = 0,
            proveedor = proveedorOrden,
            fecha_llegada = fecha
        )
        ordenPedido.save()

        ordenPedido = ORDEN_PEDIDO.objects.all().last()
        ordenPedido = ORDEN_PEDIDO.objects.get(id = ordenPedido.id)

        for listaP in listaProductos:
            
            prod = PRODUCTO.objects.get(nombre=listaP[0])

            detallePedido = DETALLE_ORDEN.objects.create(
                producto = prod,
                cantidad = listaP[1],
                orden_pedido = ordenPedido
            )
            
            correoproveedor =  "nico7vh@gmail.com"

            cuerpomensaje = "Se ha generado un pedido por favor contacte a nuestro negocio"
##


            email = EmailMessage(
                'Orden de compra - Almacen Yuyitos',
                cuerpomensaje,
                settings.EMAIL_HOST_USER,
                [correoproveedor]
            )

            email.send()

##
            detallePedido.save()
            

        messages.warning(request, 'Orden de pedido realizada con exito y correo enviado')
        return redirect('listarPedidos')

    context = {
        'proveedores':proveedores,
        'listaProds':listaProds
    }
    return render(request, 'pedidos/crear.html', context)







@login_required(login_url="login")
def PedidosDetalle(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    pedido = ORDEN_PEDIDO.objects.filter(id=id)
    detallesP = DETALLE_ORDEN.objects.filter(orden_pedido=id)
    context = {
        'pedido':pedido,
        'detallesP':detallesP,
        'id':id
    }
    return render(request, 'pedidos/detalles.html', context)

def DesactivarPedido(request, id):
    pedido = ORDEN_PEDIDO.objects.get(id = id)
    pedido.estado_recepcion = 3
    pedido.save()
    messages.warning(request, f'Pedido {pedido.id} anulado')
    return redirect('listarPedidos')

def ActivarPedido(request, id):
    pedido = ORDEN_PEDIDO.objects.get(id = id)
    pedido.estado_recepcion = 0
    pedido.save()
    messages.warning(request, f'Pedido {pedido.id} activado')
    return redirect('listarPedidos')




@login_required(login_url="login")
def CategoriasProvListar(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    categorias = CATEGORIA_PROVEEDOR.objects.all()

    return render(request, 'categoria_proveedor/listar.html', {'categorias':categorias})

@login_required(login_url="login")
def CategoriaProvCrear(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    if request.method == 'POST':

        categoria = request.POST.get('descripcion')

        categProv = CATEGORIA_PROVEEDOR.objects.create(
            descripcion = categoria
        )
        categProv.save()
        messages.warning(request, 'Categoria Proveedor creada con exito')
        return redirect('listarCategoriasProv')

    return render(request, 'categoria_proveedor/crear.html')

@login_required(login_url="login")
def CategoriaProvActualizar(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    categoriaProv = CATEGORIA_PROVEEDOR.objects.get(id=id)
    form = FormCategProv(request.POST or None, instance=categoriaProv)

    if request.method == 'POST':

        categoria = request.POST.get('descripcion')
        categoriaProv.descripcion = categoria
        categoriaProv.save()
        messages.warning(request, 'Categoria Proveedor actualizada con exito')
        return redirect('listarCategoriasProv')

    return render(request, 'categoria_proveedor/actualizar.html',{'form':form})

@login_required(login_url="login")
def BoletaListado(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    boletas = BOLETA.objects.all()

    return render(request, "boletas/listar.html", {'boletas':boletas})

@login_required(login_url="login")
def BoletaDetalle(request, id):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    boleta = BOLETA.objects.filter(id=id)
    detalles = DETALLE_BOLETA.objects.filter(boleta=id)
    context = {
        'boleta':boleta,
        'detalles':detalles,
        'id':id
    }
    return render(request, 'boletas/detalles.html', context)

def DesactivarBoleta(request, id):
    boleta = BOLETA.objects.get(id = id)
    boleta.estado = 0
    boleta.save()
    messages.warning(request, f'Boleta {boleta.id} desactivado')
    return redirect('listarBoletas')

def ActivarBoleta(request, id):
    boleta = BOLETA.objects.get(id = id)
    boleta.estado = 1
    boleta.save()
    messages.warning(request, f'Boleta {boleta.id} activado')
    return redirect('listarBoletas')

@login_required(login_url="login")
def PagosFiadosListado(request):

    usuario = request.user
    usuario = User.objects.get(username=usuario)

    pagosF = PAGO_FIADO.objects.all()

    return render(request, 'pago_fiado/listar.html', {'pagosF':pagosF})

def DesactivarPagoFiado(request, id):
    pago_fiado = PAGO_FIADO.objects.get(id = id)
    pago_fiado.estado = 0
    pago_fiado.save()
    messages.warning(request, f'Pago fiado {pago_fiado.id} desactivado')
    return redirect('pagoFiadosListar')

def ActivarPagoFiado(request, id):
    pago_fiado = PAGO_FIADO.objects.get(id = id)
    pago_fiado.estado = 1
    pago_fiado.save()
    messages.warning(request, f'Pago fiado {pago_fiado.id} activado')
    return redirect('pagoFiadosListar')

@login_required(login_url="login")
def PagarFiado(request, id = None):
    
    usuario = request.user
    usuario = User.objects.get(username=usuario)

    mostrar = ''
    if id != None:
        mostrar = 'si'
    else:
        mostrar = 'no'

    print(mostrar)

    pagos_fiados = []
    pagos_fiados2 = []
    for pag in PAGO_FIADO.objects.all():
        pagos_fiados.append(pag.id)
        pagos_fiados.append(pag.cliente.nombre)
        pagos_fiados.append(pag.monto)
        pagos_fiados.append(pag.fecha_creacion)
        pagos_fiados2.append(pagos_fiados)
        pagos_fiados = []

    for i in DETALLE_FIADO.objects.all():
        for j in pagos_fiados2:
            if i.pago_fiado.id == j[0]:
                monto = j[2] - i.monto_abonado
                j[2] = monto

    pagos_fiados = []
    for obj in pagos_fiados2:
        if obj[0] == id:
            pagos_fiados.append(obj)

    detalleF = None
    if id == None:
        pagoF = pagos_fiados2

    else: 
        pagoF = pagos_fiados
        detalleF = DETALLE_FIADO.objects.filter(pago_fiado=id)
        

    if request.method == 'POST':

        pagoRealizado = request.POST.get('pago')

        pagoFiado = PAGO_FIADO.objects.get(id=id)

        pago_detalle = DETALLE_FIADO.objects.create(
            monto_abonado = pagoRealizado,
            pago_fiado = pagoFiado
        )
        pago_detalle.save()

        messages.warning(request, 'Pago realizado con exito')
        return redirect('PagarFiadoTodos')

    context = {
        'pagoF':pagoF,
        'detalleF':detalleF,
        'mostrar':mostrar
    }

    return render(request, 'pago_fiado/pagar_fiado.html', context)
