from functools import wraps
from django.http import HttpResponseForbidden
from .models import Usuarios
#Aperturacierrecaja, 
from django.shortcuts import redirect, render

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id is None:
            return render(request, 'pages/errorPermiso.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def logout_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            user = Usuarios.objects.get(pk=user_id)
            if user.rol == 1:
                return view_func(request, *args, **kwargs)
        # Si el usuario no tiene el rol necesario, mostrar un mensaje de prohibido (forbidden)
        return render(request, 'pages/errorPermiso.html')
    return _wrapped_view

def vendedor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            user = Usuarios.objects.get(pk=user_id)
            if user.rol == 2:
                return view_func(request, *args, **kwargs)
        # Si el usuario no tiene el rol necesario, mostrar un mensaje de prohibido (forbidden)
        return render(request, 'pages/errorPermiso.html')
    return _wrapped_view
