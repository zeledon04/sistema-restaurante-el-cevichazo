# Esta vista funge/funciona tanto para la tabla productos como para la tabla platos.
# from farmacia.views import datosUser
from ..models import Categoriasproducto
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required, login_required

@login_required
def listarCategorias(request):
    # user_data = datosUser(request)
    categorias = Categoriasproducto.objects.filter(estado=1)
    
    # return render(request, 'pages/categorias/listarCategorias.html', {**user_data, 'categorias': categorias})
    return render(request, 'pages/categorias/listarCategorias.html', {'categorias': categorias})

@admin_required
def listarCategoriasInactivas(request):
    categorias = Categoriasproducto.objects.filter(estado=0)  
    # user_data = datosUser(request)
    # return render(request, 'pages/categorias/listarCategoriasInactivas.html', {**user_data, 'categorias': categorias})
    return render(request, 'pages/categorias/listarCategoriasInactivas.html', {'categorias': categorias})

@admin_required
def agregarCategoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        # Validación de campos
        categoria = Categoriasproducto(
            nombre=nombre,
            estado=1
        )
        categoria.save()
        messages.success(request, "Categoría agregada correctamente!")
        return redirect('listar_categorias')
    # user_data = datosUser(request)
    
    # return render(request, 'pages/categorias/agregarCategoria.html', user_data)
    return render(request, 'pages/categorias/agregarCategoria.html')

@admin_required
def actualizarCategoria(request, id):
    categoria = Categoriasproducto.objects.get(pk=id)
    # user_data = datosUser(request)
    # datos = {**user_data, 'categoria' : categoria}
    datos = {'categoria' : categoria}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        # Actualizar los demás campos
        categoria.nombre = nombre

        categoria.save()

        messages.success(request, "Categoría actualizada correctamente!")
        return redirect('listar_categorias')
    return render(request, 'pages/categorias/actualizarCategoria.html', datos)

@admin_required
def eliminarCategoria(request, id):
    categoria = get_object_or_404(Categoriasproducto, pk=id)
    categoria.estado = 0
    categoria.save()
    messages.success(request, "Categoría " + categoria.nombre + " eliminada correctamente.")
    return redirect('listar_categorias')

@admin_required
def activarCategoria(request, id):
    categoria = get_object_or_404(Categoriasproducto, pk=id)
    categoria.estado = 1  # Cambia el estado a activo
    categoria.save()
    messages.success(request, "Categoría " + categoria.nombre + " activada correctamente.")
    return redirect('listar_categorias')

