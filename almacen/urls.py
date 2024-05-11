
from django.contrib import admin
from django.urls import path
from src import views, static
from src.views import Index
from src.views import *
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.Login, name="login"),
    path('index/', views.Index, name="index"),
    path('venta/', views.Venta, name="venta"),
    path('recepcion/', views.RecepcionPedido, name="RecepcionPedido"),
    path('recepcion/<int:id>', views.RecepcionPedido, name="RecepcionPedido"),
    path('pagar_fiado/', views.PagarFiado, name="PagarFiadoTodos"),
    path('pagar_fiado/<int:id>', views.PagarFiado, name="PagarFiado"),


    path('clientes/', views.ClienteListado, name='listarClientes'), 
    path('clientes/crear/', views.ClienteCrear, name="crearCliente"), 
    path('clientes/detalle/<int:id>', views.ClienteDetalle, name='detalles'),
    path('clientes/editar/<int:id>', views.ClienteActualizar, name="editarCliente"),    
    path('clientes/desactivarCliente/<int:id>', views.DesactivarCliente, name="desactivarCliente"),
    path('clientes/activarCliente/<int:id>', views.ActivarCliente, name="activarCliente"),     

    path('proveedores/', views.ProveedorListado, name='listarProveedores'),    
    path('proveedores/crear/', views.ProveedorCrear, name="crearProveedor"), 
    path('proveedores/detalle/<int:id>', views.ProveedorDetalle, name='detalles'),    
    path('proveedores/editar/<int:id>', views.ProveedorActualizar, name="actualizarProveedor"),   
    path('proveedores/desactivarProveedor/<int:id>', views.DesactivarProveedor, name="desactivarProveedor"),
    path('proveedores/activarProveedor/<int:id>', views.ActivarProveedor, name="activarProveedor"),

    path('productos/', views.ProductoListado, name='listarProductos'),    
    path('productos/crear/', views.ProductoCrear, name="crearProducto"), 
    path('productos/detalle/<int:id>', views.ProductoDetalle, name='detalles'),
    path('productos/editar/<int:id>', views.ProductoActualizar, name="actualizarProducto"),    
    path('productos/desactivarProducto/<int:id>', views.DesactivarProducto, name="desactivarProducto"),
    path('productos/activarProducto/<int:id>', views.ActivarProducto, name="activarProducto"),

    path('pedidos/', views.PedidosListado, name='listarPedidos'), 
    path('pedidos/crear/', views.PedidosCrear, name="crearPedido"),
    path('pedidos/crear/<int:id>', views.PedidosCrear, name="crearPedido"),    
    path('pedidos/detalle/<int:id>', views.PedidosDetalle, name="detallePedido"),     
    path('pedidos/desactivarPedido/<int:id>', views.DesactivarPedido, name="desactivarPedido"),
    path('pedidos/activarPedido/<int:id>', views.ActivarPedido, name="activarPedido"),

    path('boletas/', views.BoletaListado, name="listarBoletas"),
    path('boletas/detalle/<int:id>', views.BoletaDetalle, name="detallesBoleta"),
    path('boletas/desactivarBoleta/<int:id>', views.DesactivarBoleta, name="desactivarBoleta"),
    path('boletas/activarBoleta/<int:id>', views.ActivarBoleta, name="activarBoleta"),

    path('tipos_productos/', views.TipoProductoListado, name='listarTiposProductos'),
    path('tipos_productos/crear/', views.TipoProductoCrear, name="crearTipoProducto"),
    path('tipos_productos/editar/<int:id>', views.TipoProductoActualizar, name="actualizarTipoProducto"),

    path('familias_productos/', views.FamiliaProductoListado, name='listarFamiliasProductos'),
    path('familias_productos/crear/', views.FamiliaProductoCrear, name="crearFamiliaProducto"),
    path('familias_productos/editar/<int:id>', views.FamiliaProductoActualizar, name="actualizarFamiliaProducto"),

    path('categoria_proveedor/', views.CategoriasProvListar, name="listarCategoriasProv"),
    path('categoria_proveedor/crear/', views.CategoriaProvCrear, name="crearCategoriaProv"),
    path('categoria_proveedor/editar/<int:id>', views.CategoriaProvActualizar, name="actualizarCategoriaProv"),

    path('fiados/', views.PagosFiadosListado, name='pagoFiadosListar'),
    path('fiados/desactivarPagoFiado/<int:id>', views.DesactivarPagoFiado, name="desactivarPagoFiado"),
    path('fiados/activarPagoFiado/<int:id>', views.ActivarPagoFiado, name="activarPagoFiado"),

]

