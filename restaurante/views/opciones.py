from ..utils import admin_required, logout_required, login_required
from django.contrib.auth import logout, authenticate
from ..models import Opciones
from django.contrib import messages
from django.shortcuts import render, redirect
from ..view import datosUser

@admin_required
def opciones(request):
    user_data = datosUser(request)
    opc = Opciones.objects.first()
    datos = {**user_data, 'opcion': opc}
    if request.method == 'POST':
        tasa = request.POST.get('tasa')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')
        numeroruc = request.POST.get('numeroruc')
        nombreImpresora = request.POST.get('nombreImpresora')
        
        if tasa:
            try:
                tasa = float(tasa)
                if tasa <= 0:
                    messages.error(request, "La tasa Inválida.")
                else:
                    opc.tasacambio = tasa
                    # messages.success(request, "Tasa de cambio actualizada correctamente.")
            except ValueError:
                messages.error(request, "Por favor, ingresa un valor numérico válido para la tasa de cambio.")    
        opc.direccion = direccion
        opc.telefono = telefono
        opc.mensaje = mensaje
        opc.numeroruc = numeroruc
        opc.nombreimpresora = nombreImpresora
        opc.save()
        messages.success(request, "Configuración actualizada correctamente!")    
    return render(request, 'pages/opciones/opciones.html', datos)