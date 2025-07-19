from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from restaurante.models import Categoriasproducto, Platos
import os
from datetime import datetime, timedelta

def listarPlatos(request):
    categorias = Categoriasproducto.objects.filter(estado=1)
    platos = Platos.objects.filter(estado=1).select_related('categoriaid').order_by('-platoid')

    datos = {'categorias':categorias, 'platos': platos}
    
    return render(request, 'pages/platos/listarPlatos.html', datos)


def listarPlatosInactivos(request):
    categorias = Categoriasproducto.objects.filter(estado=1)
    platos = Platos.objects.filter(estado=0).select_related('categoriaid').order_by('-platoid')
    
    datos = {'categorias':categorias, 'platos': platos}
    
    return render(request, 'pages/platos/listarPlatosInactivos.html', datos)


def agregarPlato(request):
    categorias = Categoriasproducto.objects.filter(estado = 1)
    datos = {'categorias':categorias}
    
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            categoriaid = request.POST.get('categoriaid')
            precio = request.POST.get('precio')
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
            
            platos = Platos(
                nombre = nombre,
                descripcion  = descripcion,
                categoriaid_id = categoriaid,
                precio = precio,
                estado = 1,
                rutafoto = ruta,
                updated_at = timezone.now()
            )
            platos.save()
            messages.success(request, 'Platillo agregado correctamente!')
            return redirect('listar_platos')
    except Exception as e:
        messages.error(request, f"Error al agregar el platillo: {str(e)}")
        return redirect('agregar_plato')
    return render(request, 'pages/platos/agregarPlato.html', datos)


def  actualizarPlato(request, id):
    categorias = Categoriasproducto.objects.filter(estado=1)
    plato = Platos.objects.get(pk=id)
    
    datos = { 'plato':plato, 'categorias': categorias}
    
    try:
    
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
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
                plato.rutafoto = filename
                
            plato.nombre = nombre
            plato.descripcion = descripcion
            plato.categoriaid_id = categoriaid
            plato.precio = precio
            plato.updated_at = timezone.now()
            
            plato.save()
            messages.success(request, "Plato actualizado correctamente!")
            return redirect('listar_platos')
    except Exception as e:
            messages.error(request, f"Error al agregar el plato: {str(e)}")
            return redirect('actualizar_plato', id=id)
        
    return render(request, 'pages/platos/actualizarPlato.html', datos)

def eliminarPlato(request, id):
    platos = get_object_or_404(Platos, pk=id)
    platos.estado = 0
    platos.save()
    messages.success(request, "Plato " + platos.nombre + " eliminado correctamente.")
    return redirect('listar_platos')

def activarPlato(request, id):
    plato = get_object_or_404(Platos, pk=id)
    plato.estado = 1  # Cambia el estado a activo
    plato.save()
    messages.success(request, "Plato " + plato.nombre + " activado correctamente.")
    return redirect('listar_platos')

