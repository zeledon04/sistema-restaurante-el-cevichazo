from datetime import date, timedelta
from ..view import datosUser
from ..models import Usuarios
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ..utils import admin_required
from django.contrib.auth.hashers import make_password, check_password

@admin_required
def listarUsuarios(request):
    user_data = datosUser(request)
    usuarios = Usuarios.objects.filter(estado=1)
    
    return render(request, 'pages/usuarios/listarUsuarios.html', {**user_data, 'usuarios': usuarios})

@admin_required
def listarUsuariosInactivos(request):
    user_data = datosUser(request)
    usuarios = Usuarios.objects.filter(estado=0)
    return render(request, 'pages/usuarios/listarUsuariosInactivos.html', {**user_data, 'usuarios': usuarios})

@admin_required
def agregarUsuario(request):
    user_data = datosUser(request)
    datos = {**user_data}
    

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rol = request.POST.get('rol')
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        telefono = request.POST.get('telefono')
        
        contra_cifrada = make_password(contrasena)
        
        # Validación de campos
        usuario = Usuarios(
            nombre=nombre,
            rol=rol,
            user=usuario,
            contra=contra_cifrada,
            telefono=telefono,
            estado=1
        )
        usuario.save()
        messages.success(request, "Usuario agregado correctamente!")
        return redirect('listar_usuarios')
    return render(request, 'pages/usuarios/agregarUsuario.html', datos)

@admin_required
def actualizarUsuario(request, id):
    usuario = Usuarios.objects.get(pk=id)
    user_data = datosUser(request)
    datos = {**user_data, 'usuario' : usuario}
    
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            rol = request.POST.get('rol')
            usuarioNombre = request.POST.get('usuario')
            contrasena = request.POST.get('contrasena')
            telefono = request.POST.get('telefono')
        except Usuarios.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('listar_usuarios')

        # Actualizar los demás campos
        if contrasena:
            contra_cifrada = make_password(contrasena)

            usuario.contra = contra_cifrada
        usuario.nombre = nombre
        usuario.telefono = telefono
        usuario.user = usuarioNombre
       
        usuario.rol = rol

        usuario.save()
        return redirect('logout')
    return render(request, 'pages/usuarios/actualizarUsuario.html', datos)

@admin_required
def eliminarUsuario(request, id):
    usuario = get_object_or_404(Usuarios, pk=id)
    usuario.estado = 0
    usuario.save()
    messages.success(request, "Usuario " + usuario.nombre + " Eliminado Correctamente.")
    return redirect('listar_usuarios')

@admin_required
def activarUsuario(request, id):
    usuario = get_object_or_404(Usuarios, pk=id)
    usuario.estado = 1  # Cambia el estado a activo
    usuario.save()
    messages.success(request, "Usuario " + usuario.nombre + " Activado Correctamente.")
    return redirect('listar_usuarios')
