from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator 
from django.utils import timezone
from restaurante.models import Categoriasproducto, Detallefacturaplato, Detallefacturaproducto, Productos
import os
from datetime import datetime, timedelta
from ..utils import login_required, admin_required
from ..view import datosUser
from itertools import chain 

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
    
    user_data = datosUser(request)
    return render(request, 'pages/productos/listarProductos.html', {
        **user_data,
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
    
    user_data = datosUser(request)
    return render(request, 'pages/productos/listarProductosInactivos.html', {
        **user_data,
        'productos': page_obj,
        'categorias':categorias
    })

@admin_required
def agregarProducto(request):
    categorias = Categoriasproducto.objects.filter(estado = 1)
    user_data = datosUser(request)
    datos = {**user_data, 'categorias': categorias}   
    
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoriaid = request.POST.get('categoriaid')
            ruta = 'defaultImage.png'

        if 'rutafoto' in request.FILES:
            file = request.FILES['rutafoto']
            filename = nombre.replace(" ", "") + '.jpg'
            # full_path = os.path.join(settings.BASE_DIR, 'restaurante/static/productos/', filename)
            
            # Ruta de almacenamiento segura para usuarios finales
            user_static_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'media', 'productos')
            os.makedirs(user_static_dir, exist_ok=True)
            full_path = os.path.join(user_static_dir, filename)

            # Guardar archivo en el sistema
            with open(full_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
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
    user_data = datosUser(request)
    datos = {**user_data, 'producto': producto, 'categorias': categorias}
    
    try:
    
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoriaid = request.POST.get('categoriaid')
            
            user_static_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'media', 'productos')
            os.makedirs(user_static_dir, exist_ok=True)  # Asegura que el directorio exista
            filename = nombre.replace(" ", "") + ".jpg"
            nueva_ruta_absoluta = os.path.join(user_static_dir, filename)
            ruta_anterior_rel = producto.rutafoto
            ruta_anterior_absoluta = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', ruta_anterior_rel.replace('/', os.sep))

            if 'rutafoto' in request.FILES:
                file = request.FILES['rutafoto']

                with open(nueva_ruta_absoluta, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                        
                if ruta_anterior_rel != 'defaultImage.png' and os.path.exists(ruta_anterior_absoluta):
                    os.remove(ruta_anterior_absoluta)
            
                producto.rutafoto = filename
            elif ruta_anterior_rel != 'defaultImage.png' and os.path.exists(ruta_anterior_absoluta):
                if os.path.exists(ruta_anterior_absoluta) != filename:
                    nueva_ruta_absoluta = os.path.join(user_static_dir, filename)
                    os.rename(ruta_anterior_absoluta, nueva_ruta_absoluta)
                    producto.rutafoto = filename
                    
            try:
                producto.nombre = nombre
                producto.descripcion = descripcion
                producto.categoriaid_id = categoriaid
                producto.updated_at = timezone.now()
                
                producto.save()
                messages.success(request, "¡Producto actualizado correctamente!")    
                return redirect('listar_productos')
            except Exception as e:
                messages.error(request, f"Error al actualizar el producto: {str(e)}")
                return redirect('actualizar_producto', id=id)
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
def historialVentas(request):
    productos = list(Detallefacturaproducto.objects.filter(estado=1).select_related('facturaid'))
    platos = list(Detallefacturaplato.objects.filter(estado=1).select_related('facturaid'))

    # Etiquetar el tipo, por si quieres mostrarlo en la vista
    for p in productos:
        p.tipo = 'producto'
        p.total = p.cantidad * p.preciounitario
    
    for p in platos:
        p.tipo = 'plato'
        p.total = p.cantidad * p.preciounitario

    # Combinar y ordenar por detalleid descendente
    ventas = sorted(chain(productos, platos), key=lambda x: x.facturaid.fecha, reverse=True)

    # Paginación manual
    paginator = Paginator(ventas, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Contador global
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for venta in page_obj:
        venta.cont = cont
        cont += 1
        
    user_data = datosUser(request)
    datos = {**user_data, 'ventas': page_obj}
    return render(request, 'pages/productos/historialVentas.html', datos)



@login_required
def filtrar_productos(request):
    
    nombre = request.GET.get('nombre', '')
    categoria = request.GET.get('categoria', '')
    print(f"Filtrando productos por nombre: {nombre} y categoría: {categoria}")

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

from django.db.models import Q

@login_required
def filtrar_ventas(request):
    nombre = request.GET.get("nombre")
    fecha_filtro = request.GET.get("fecha")
    fecha_inicio = request.GET.get("inicio")
    fecha_fin = request.GET.get("fin")

    # Obtener los filtros de fecha
    fecha_filter = Q()
    hoy = datetime.now().date()

    if fecha_filtro == "hoy":
        fecha_filter = Q(facturaid__fecha__date=hoy)
    elif fecha_filtro == "semana":
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)
        fecha_filter = Q(facturaid__fecha__date__range=[inicio_semana, fin_semana])
    elif fecha_filtro == "mes":
        ahora = datetime.now()
        fecha_filter = Q(facturaid__fecha__year=ahora.year, facturaid__fecha__month=ahora.month)
    elif fecha_filtro == "anio":
        ahora = datetime.now()
        fecha_filter = Q(facturaid__fecha__year=ahora.year)
    elif fecha_filtro == "rango" and fecha_inicio and fecha_fin:
        fecha_filter = Q(facturaid__fecha__date__range=[fecha_inicio, fecha_fin])

    # QuerySet para productos
    productos_qs = Detallefacturaproducto.objects.filter(estado=1)
    if nombre:
        productos_qs = productos_qs.filter(productoid__nombre__istartswith=nombre)
    productos_qs = productos_qs.filter(fecha_filter)

    # QuerySet para platos
    platos_qs = Detallefacturaplato.objects.filter(estado=1)
    if nombre:
        platos_qs = platos_qs.filter(platoid__nombre__istartswith=nombre)
    platos_qs = platos_qs.filter(fecha_filter)

    # Combinar resultados
    data = []
    cont = 1

    for venta in productos_qs.order_by('-detalleid'):
        data.append({
            'cont': cont,
            'producto': venta.productoid.nombre,
            'fecha': venta.facturaid.fecha.strftime("%d/%m/%Y %I:%M %p") if venta.facturaid.fecha else '',
            'cantidad': venta.cantidad,
            'precio': venta.preciounitario,
            'precioCompra': venta.preciocompra,
            'tipo': 'producto'
        })
        cont += 1

    for venta in platos_qs.order_by('-detalleid'):
        data.append({
            'cont': cont,
            'producto': venta.platoid.nombre,
            'fecha': venta.facturaid.fecha.strftime("%d/%m/%Y %I:%M %p") if venta.facturaid.fecha else '',
            'cantidad': venta.cantidad,
            'precio': venta.preciounitario,
            'precioCompra': '',  # Puedes omitirlo o dejarlo en blanco si no aplica
            'tipo': 'plato'
        })
        cont += 1

    # Opcional: puedes ordenar `data` por fecha descendente si lo deseas
    data.sort(key=lambda x: datetime.strptime(x['fecha'], "%d/%m/%Y %I:%M %p"), reverse=True)

    return JsonResponse({'ventas': data})

