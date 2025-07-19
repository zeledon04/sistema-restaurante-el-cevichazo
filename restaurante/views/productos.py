from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator 
from django.utils import timezone
from restaurante.models import Categoriasproducto, Productos
import os
from datetime import datetime, timedelta
from ..utils import login_required, admin_required

# Create your views here.
@login_required
def listarProductos(request):
    categorias = Categoriasproducto.objects.filter(estado=1)
    productos_set = Productos.objects.filter(estado=1).select_related('categoriaid').order_by('-productoid')
    
    paginator = Paginator(productos_set, 50)
    
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for producto in page_obj:
        producto.cont = cont 
        cont += 1
    
    return render(request, 'pages/productos/listarProductos.html', {
        'productos': page_obj,
        'categorias':categorias
    })

@admin_required
def listarProductosInactivos(request):
    categorias = Categoriasproducto.objects.filter(estado=1)
    productos_set = Productos.objects.filter(estado=0).select_related('categoriaid').order_by('-productoid')
    
    paginator = Paginator(productos_set, 50)
    
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for producto in page_obj:
        producto.cont = cont 
        cont += 1
    
    return render(request, 'pages/productos/listarProductosInactivos.html', {
        'productos': page_obj,
        'categorias':categorias
    })

@admin_required
def agregarProducto(request):
    categorias = Categoriasproducto.objects.filter(estado = 1)
    datos = {'categorias':categorias}
    
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoriaid = request.POST.get('categoriaid')
            ruta = 'defaultImage.png'

        if 'rutafoto' in request.FILES:
            file = request.FILES['rutafoto']
            filename = nombre.replace(" ", "") + '.jpg'
            full_path = os.path.join(settings.BASE_DIR, 'restaurante/static/productos/', filename)
            
            # Ruta de almacenamiento segura para usuarios finales
            # user_static_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'media', 'productos')
            # os.makedirs(user_static_dir, exist_ok=True)
            # full_path = os.path.join(user_static_dir, filename)

            # Guardar archivo en el sistema
            with open(full_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # Guardar ruta relativa para mostrar con {% static %}
            # rel_path = os.path.relpath(full_path, os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante'))
            # ruta = rel_path.replace('\\', '/')
            ruta = filename
            
            producto = Productos(
                nombre = nombre,
                descripcion  = descripcion,
                categoriaid_id = categoriaid,
                precio = 0,
                stock = 0,
                estado = 1,
                rutafoto = ruta,
                updated_at = timezone.now()
            )
            producto.save()
            messages.success(request, '¡Producto agregado correctamente!')
            return redirect('listar_productos')
    except Exception as e:
        messages.error(request, f"Error al agregar el producto: {str(e)}")
        return redirect('agregar_producto')
    return render(request, 'pages/productos/agregarProducto.html', datos)

@admin_required
def  actualizarProducto(request, id):
    categorias = Categoriasproducto.objects.filter(estado=1)
    producto = Productos.objects.get(pk=id)
    
    datos = { 'producto':producto, 'categorias': categorias}
    
    try:
    
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoriaid = request.POST.get('categoriaid')
            
            if 'rutafoto' in request.FILES:
                file = request.FILES['rutafoto']
                filename = nombre.replace(" ", "") + ".jpg"
                full_path = os.path.join(settings.BASE_DIR, 'restaurante/static/productos', filename)
                
                #Guardar la nueva imagen
                with open(full_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                #Actualizar ruta de imagen
                producto.rutafoto = filename
                
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.categoriaid_id = categoriaid
            producto.updated_at = timezone.now()
            
            producto.save()
            messages.success(request, "¡Producto actualizado correctamente!")    
            return redirect('listar_productos')
    except Exception as e:
            messages.error(request, f"Error al agregar el producto: {str(e)}")
            return redirect('actualizar_producto', id=id)
        
    return render(request, 'pages/productos/actualizarProducto.html', datos)

@admin_required
def eliminarProducto(request, id):
    producto = get_object_or_404(Productos, pk=id)
    producto.estado = 0
    producto.save()
    messages.success(request, "Producto " + producto.nombre + " eliminado correctamente.")
    return redirect('listar_productos')

@admin_required
def activarProducto(request, id):
    producto = get_object_or_404(Productos, pk=id)
    producto.estado = 1  # Cambia el estado a activo
    producto.save()
    messages.success(request, "Producto " + producto.nombre + " activada correctamente.")
    return redirect('listar_productos')

@login_required
def filtrar_productos(request):
    nombre = request.GET.get('nombre', '')
    categoria = request.GET.get('categoria', '')

    productos = Productos.objects.filter(estado=1).order_by('-productoid')

    if nombre:
        productos = productos.filter(nombre__istartswith=nombre)
    if categoria:
        productos = productos.filter(categoriaid_id=categoria)

    data = []
    for i, p in enumerate(productos, 1):
        data.append({
            'cont': i,
            'productoid': p.productoid,
            'nombre': p.nombre,
            'rutafoto': p.rutafoto,
            'categoria': p.categoriaid.nombre,
            'stock': p.stock,
            'precio': str(p.precio),
            'updated_at': int(p.updated_at.timestamp())  # para refrescar la imagen
        })

    return JsonResponse(data, safe=False)
