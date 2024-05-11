from django import forms
from .models import BOLETA, CATEGORIA_PROVEEDOR, CLIENTE, FAMILIA_PRODUCTO, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO, TIPO_PRODUCTO

   
class FormCliente(forms.ModelForm):
    
    class Meta:
        model = CLIENTE
        fields = ("run","nombre","telefono","correo","direccion")

class FormProductoEdit(forms.ModelForm):
    
    class Meta:
        model = PRODUCTO
        fields = ("nombre","precio","descripcion","precio_compra","stock","stock_critico","codigo_barra","familia_producto")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control'  
            })  
        self.fields['codigo_barra'].widget.attrs['readonly'] = True 
        self.fields['precio'].widget.attrs['readonly'] = True

class FormProducto(forms.ModelForm):
    
    class Meta:
        model = PRODUCTO
        fields = ("familia_producto",)

class FormFamiliaProd(forms.ModelForm):
    
    class Meta:
        model = FAMILIA_PRODUCTO
        fields = ("tipo_producto","descripcion")

class FormProductoProv(forms.ModelForm):
    
    class Meta:
        model = ORDEN_PEDIDO
        fields = ("proveedor",)

class FormCategProv(forms.ModelForm):
    
    class Meta:
        model = CATEGORIA_PROVEEDOR
        fields = ("descripcion",)

class FormClientesParaVenta(forms.ModelForm):
    
    class Meta:
        model = BOLETA
        fields = ("cliente",)

class FormTipoProducto(forms.ModelForm):

    class Meta:
        model = TIPO_PRODUCTO
        fields = ("descripcion","proveedor")

class FormProveedor(forms.ModelForm):

    class Meta:
        model = PROVEEDOR
        fields = ("categoria_proveedor",)

class FormProveedorAct(forms.ModelForm):
    
    class Meta:
        model = PROVEEDOR
        fields = ("razon_social","correo","telefono","direccion","categoria_proveedor")

class FormPedido(forms.ModelForm):
    
    class Meta:
        model = ORDEN_PEDIDO
        fields = ("proveedor",) 




    