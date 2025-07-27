from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Mesas, Cocinas, Platos
from django.http import JsonResponse
from ..view import datosUser
from django.views.decorators.csrf import csrf_exempt
from ..utils import login_required
from datetime import datetime, date
from django.utils import timezone
from django.templatetags.static import static
from django.utils.dateformat import format

import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def listarCocinas(request):
    user_data = datosUser(request)
    datos = {
        **user_data, 
    }
    # Render the template with the list of kitchens
    return render(request, 'pages/cocinas/listarCocinas.html', datos)

def cocina_estado(request):
    datos =[]
    cocinas = Cocinas.objects.filter(estado__in=[0, 1, 2])
    for cocina in cocinas:
        
        hora_mostrar = None
        if cocina.estado == 0:
            hora_mostrar = format(cocina.hora, 'c')
        elif cocina.estado == 1:
            hora_mostrar = format(cocina.horafinalizada, 'c')
        elif cocina.estado == 2:
            hora_mostrar = format(cocina.horapreparacion, 'c')

        mesaOnombre = None
        if not cocina.mesaid:
            mesaOnombre = cocina.cliente
        else:
            mesaOnombre = cocina.mesaid.numero
            
        
        datos.append({
            "cocinaid": cocina.cocinaid,
            "plato": cocina.platoid.nombre,
            "imagen": static('productos/' + str(cocina.platoid.rutafoto)) if cocina.platoid.rutafoto else static('img/defaultImage.png'),
            "hora": hora_mostrar,
            "estado": cocina.estado,
            "mesa": mesaOnombre,
        })
        
    return JsonResponse({"datos":datos})

@csrf_exempt
def cambiar_estado_cocina(request, cocina_id):
    if request.method == "POST":
        data = json.loads(request.body)
        nuevo_estado = data.get("estado")
        print(f"Cambiando estado de cocina {cocina_id} a {nuevo_estado}")

        cocina = Cocinas.objects.get(pk=cocina_id)
        cocina.estado = nuevo_estado

        if nuevo_estado == 2:  # En Proceso
            cocina.horapreparacion = timezone.now()
        elif nuevo_estado == 1:  # Listo
            cocina.horafinalizada = timezone.now()

        cocina.save()
        return JsonResponse({"success": True})


def enviar_a_cocina(request):
    body = json.loads(request.body)
    front = body.get("front")
    print("Front value:", front)
    numeroMesa = body.get("mesaId")
    nombreCliente = body.get("nombreCliente")
    platoId = body.get("platoId")
    if front == "1":
        mesa = Mesas.objects.filter(mesaid=numeroMesa).first()
        
    else:
        mesa = Mesas.objects.filter(numero=numeroMesa).first()
        if not mesa:
            mesa = None

    # Crear registro en cocina
    try:
        cocinas = Cocinas(
            mesaid=mesa,
            platoid_id=platoId,
            estado=0,  # Pendiente por defecto
            hora=timezone.now(),
            cliente=nombreCliente if nombreCliente else None,
        )
        cocinas.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        print(f"Error al enviar a cocina: {e}")
        return JsonResponse({"status": "error"})
    
