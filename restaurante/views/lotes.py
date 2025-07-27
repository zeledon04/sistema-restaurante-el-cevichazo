from datetime import datetime
# from farmacia.views import datosUser
from ..models import Lotesproductos, Productos, Usuarios
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required

from django.db.models import Case, When, Value, IntegerField

from ..view import datosUser

@admin_required
def listarLotes(request, id):
    producto = Productos.objects.get(pk=id)
    lotes = (
        Lotesproductos.objects
        .exclude(estado=0)
        .filter(productoid = id)
        .annotate (
            prioridad = Case (
                When(estado=1, then=Value(0)),  
                When(estado=3, then=Value(1)), 
                When(estado=2, then=Value(2)),  
                default=Value(3),       
                output_field=IntegerField()
            )
        )
        .order_by('prioridad', 'loteid')
    )
    user_data = datosUser(request)
    datos = {**user_data, 'lotes': lotes, 'producto': producto}
    return render(request, 'pages/productos/lotes/listarLotes.html', datos)

@admin_required
def agregarLote(request, id):
    producto = Productos.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'producto' : producto}
    
    if request.method == 'POST':
        fechavencimiento = request.POST.get('fechavencimiento')
        preciocompraunitario = request.POST.get('preciocompraunitario')
        precioventa = request.POST.get('precioventa')
        cantidad = request.POST.get('cantidad')
        totalStock = int(cantidad) + producto.stock
        producto.stock = totalStock
        
        if float(precioventa) < float(preciocompraunitario):
            print("El precio de venta no puede ser menor al precio de compra.")
            messages.error(request, "Verifique los datos. El precio de venta no puede ser menor al precio de compra.")
            return redirect('agregar_lote', id=producto.productoid)
    
        if (float(precioventa) <= 0.0) or (float(preciocompraunitario) <= 0.0):
            messages.error(request, "Datos Invalidos.")
            return redirect('agregar_lote', id=producto.productoid)
        
        estado = 1
        if Lotesproductos.objects.filter(productoid=producto).exclude(estado=0).exists():
            estado = 3
            pass
        else:
            producto.precio = precioventa
            
        if Lotesproductos.objects.filter(productoid=producto, estado=1).exists():
            pass
        else:
            producto.precio = precioventa
            estado = 1
            
        lote = Lotesproductos(
            fechaingreso=datetime.today().date(),
            fechavencimiento=fechavencimiento,
            preciocompraunitario=preciocompraunitario,
            precioventa = precioventa,
            cantidad=cantidad,
            productoid_id=producto.productoid,
            estado=estado,
            stock=cantidad,
        )
        
        producto.save()
        lote.save()
        messages.success(request, "Lote agregado correctamente!")
        return redirect('listar_productos')
    return render(request, 'pages/productos/lotes/agregarLote.html', datos)

@admin_required
def cerrarLote(request, id):
    lotes = get_object_or_404(Lotesproductos, loteid=id)
    if int(lotes.estado) == 3:
        messages.warning(request, "Lote en espera no se puede cerrar")
        return redirect('listar_lotes', id=lotes.productoid.productoid)
        
    lotes.estado = 2  # Cambia el estado a 2 --> Cerrar el lote
    lotes.save()
    
    messages.success(request, "Lote cerrado correctamente!")
    return redirect('listar_lotes', id=lotes.productoid.productoid)  # Redirige a la lista de lotes del producto

@admin_required
def eliminarLote(request, id):
    lotes = get_object_or_404(Lotesproductos, loteid=id)
    
    if lotes.estado == 2:
        messages.error(request, "No se puede eliminar un lote cerrado.")
        return redirect('listar_lotes', id=lotes.productoid.productoid)
    else:
        lotes.estado = 0  # Cambia el estado a 0 --> Eliminar el lote
        producto = lotes.productoid
        producto.stock -= lotes.cantidad  # Resta la cantidad del lote al stock del producto
        lotes.save()  # Guarda el cambio en el estado del lote
        producto.save()  # Guarda el cambio en el stock del producto

        messages.success(request, "Lote eliminado correctamente!")
        return redirect('listar_lotes', id=producto.productoid)  # Redirige a la lista de lotes del producto