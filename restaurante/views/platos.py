from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from restaurante.models import Categoriasproducto, Platos
import os
from datetime import datetime, timedelta
from ..view import datosUser
from django.db import transaction

from ..utils import admin_required, login_required
@login_required
def listarPlatos(request):
    
    platos = Platos.objects.filter(estado=1).select_related('categoriaid').order_by('-platoid')
    user_data = datosUser(request)
    datos = {**user_data,'platos': platos}
        
    return render(request, 'pages/platos/listarPlatos.html', datos)

@admin_required
def listarPlatosInactivos(request):
    categorias = Categoriasproducto.objects.filter(estado=1)
    platos = Platos.objects.filter(estado=0).select_related('categoriaid').order_by('-platoid')
    user_data = datosUser(request)
    datos = {**user_data, 'categorias': categorias, 'platos': platos}
    
    return render(request, 'pages/platos/listarPlatosInactivos.html', datos)

@admin_required
@transaction.atomic
def agregarPlato(request):
    user_data = datosUser(request)
    categorias = Categoriasproducto.objects.filter(estado=1)
    datos = {**user_data, 'categorias': categorias}

    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoriaid = request.POST.get('categoriaid')
            precio = request.POST.get('precio')
            tiempo_estimado = request.POST.get('tiempo')
            ruta = 'defaultImage.png'

            plato = Platos(
                nombre = nombre,
                descripcion  = descripcion,
                categoriaid_id = categoriaid,
                precio = precio,
                estado = 1,
                tiempo = tiempo_estimado,
                rutafoto = ruta,
                updated_at = timezone.now()
            )
            plato.save()
            
        if 'rutafoto' in request.FILES:
            file = request.FILES['rutafoto']
            limpio = nombre.replace(" ", "")
            filename = f"{limpio}_{plato.platoid}.jpg"
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
            
            plato.rutafoto = ruta
            plato.save()
            
            
            messages.success(request, 'Platillo agregado correctamente!')
            return redirect('listar_platos')
    except Exception as e:
        messages.error(request, f"Error al agregar el platillo: {str(e)}")
        return redirect('agregar_plato')
    return render(request, 'pages/platos/agregarPlato.html', datos)

@admin_required
def  actualizarPlato(request, id):
    categorias = Categoriasproducto.objects.filter(estado=1)
    plato = Platos.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'plato': plato, 'categorias': categorias}
    
    try:
    
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            categoriaid = request.POST.get('categoriaid')
            timepo_estimado = request.POST.get('tiempo')
            
            user_static_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'media', 'productos')
            os.makedirs(user_static_dir, exist_ok=True)  # Asegura que el directorio exista
            filename = nombre.replace(" ", "") + ".jpg"
            nueva_ruta_absoluta = os.path.join(user_static_dir, filename)
            ruta_anterior_rel = plato.rutafoto
            ruta_anterior_absoluta = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', ruta_anterior_rel.replace('/', os.sep))
            
            
            if 'rutafoto' in request.FILES:
                file = request.FILES['rutafoto']
                
                #Guardar la nueva imagen
                with open(nueva_ruta_absoluta, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                if ruta_anterior_rel != 'defaultImage.png' and os.path.exists(ruta_anterior_absoluta):
                    os.remove(ruta_anterior_absoluta)
                    
                #Actualizar ruta de imagen
                plato.rutafoto = filename
            elif ruta_anterior_rel == 'defaultImage.png' and not os.path.exists(ruta_anterior_absoluta):
                if os.path.exists(ruta_anterior_absoluta):
                    if os.path.exists(ruta_anterior_absoluta) != filename:
                        nueva_ruta_absoluta = os.path.join(user_static_dir, filename)
                        os.rename(ruta_anterior_absoluta, nueva_ruta_absoluta)
                        plato.rutafoto = filename
            
            try:
                plato.nombre = nombre
                plato.descripcion = descripcion
                plato.categoriaid_id = categoriaid
                plato.precio = precio
                plato.tiempo = timepo_estimado
                plato.updated_at = timezone.now()
                
                plato.save()
                messages.success(request, "Plato actualizado correctamente!")
                return redirect('listar_platos')
            except Exception as e:
                messages.error(request, f"Error al actualizar el plato: {str(e)}")
                return redirect('actualizar_plato', id=id)
            
    except Exception as e:
            messages.error(request, f"Error al agregar el plato: {str(e)}")
            return redirect('actualizar_plato', id=id)
        
    return render(request, 'pages/platos/actualizarPlato.html', datos)

@admin_required
def eliminarPlato(request, id):
    platos = get_object_or_404(Platos, pk=id)
    platos.estado = 0
    platos.save()
    messages.success(request, "Plato " + platos.nombre + " eliminado correctamente.")
    return redirect('listar_platos')

@admin_required
def activarPlato(request, id):
    plato = get_object_or_404(Platos, pk=id)
    plato.estado = 1  # Cambia el estado a activo
    plato.save()
    messages.success(request, "Plato " + plato.nombre + " activado correctamente.")
    return redirect('listar_platos')

