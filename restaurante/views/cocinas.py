from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Mesas, Cocinas
from django.http import JsonResponse
from ..view import datosUser
from django.views.decorators.csrf import csrf_exempt
from ..utils import login_required
import json

@login_required
def listarCocinas(request):
    user_data = datosUser(request)
    datos = {**user_data}
    # Render the template with the list of kitchens
    return render(request, 'pages/cocinas/listarCocinas.html', datos)

def cocina_estado(request):
    datos = list(Cocinas.objects.values())  # Puedes filtrar si es necesario
    return JsonResponse(datos, safe=False)

def enviar_a_cocina(request):
    body = json.loads(request.body)
    mesaId = body.get("mesaId")
    platoId = body.get("platoId")  
    detalleId = body.get("detalleId")
    if not mesaId or not platoId or not detalleId:
        return JsonResponse({"status": "error", "message": "Datos incompletos."}, status=400)
    print(f"Enviando a cocina: Mesa {mesaId}, Plato {platoId}, Detalle {detalleId}")
    # mesaId = request.POST.get("mesaId")
    # platoId = request.POST.get("platoId")
    # detalleId = request.POST.get("detalleId")

    # Crear registro en cocina
    Cocinas.objects.create(
        mesaid_id=mesaId,
        platoid=platoId,
        detalleid=detalleId,
        estado=0  # Pendiente por defecto
    )
    # Redirigir o devolver json para AJAX (ver abajo)
    return JsonResponse({"status": "success"})