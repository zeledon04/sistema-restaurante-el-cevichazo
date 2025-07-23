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
import json

@login_required
def listarCocinas(request):
    user_data = datosUser(request)
    mesas = Mesas.objects.filter(estado=1).order_by('mesaid')
    platos = Cocinas.objects.filter(estado=1).order_by('platoid__platoid')
    cocinas = Cocinas.objects.filter(estado=0).order_by('cocinaid')
    datos = {
        **user_data, 
        'mesas': mesas,
        'cocinas': cocinas,
        'platos': platos,
    }
    # Render the template with the list of kitchens
    return render(request, 'pages/cocinas/listarCocinas.html', datos)

def cocina_estado(request):
    datos =[]
    cocinas = Cocinas.objects.filter(estado__in=[0, 1, 2])
    for cocina in cocinas:
        # Convertir TimeField a datetime con la fecha de hoy
        hora_iso = datetime.combine(date.today(), cocina.hora).isoformat() if cocina.hora else None
        prep_iso = datetime.combine(date.today(), cocina.horapreparacion).isoformat() if cocina.horapreparacion else None
        fin_iso = datetime.combine(date.today(), cocina.horafinalizada).isoformat() if cocina.horafinalizada else None
        
        datos.append({
            "cocinaid": cocina.cocinaid,
            "plato": cocina.platoid.nombre,
            "imagen": static('productos/' + str(cocina.platoid.rutafoto)) if cocina.platoid.rutafoto else static('img/defaultImage.png'),
            "hora": hora_iso,
            "horapreparacion": prep_iso,
            "horafinalizada": fin_iso,
            "estado": cocina.estado,    
            "mesa": cocina.mesaid.numero if cocina.mesaid else None,
        })
        
    return JsonResponse({"datos":datos})

@csrf_exempt
def cambiar_estado_cocina(request, cocina_id):
    if request.method == "POST":
        data = json.loads(request.body)
        nuevo_estado = data.get("estado")

        cocina = Cocinas.objects.get(pk=cocina_id)
        cocina.estado = nuevo_estado

        if nuevo_estado == 2:  # En Proceso
            cocina.horapreparacion = timezone.now().time()
        elif nuevo_estado == 1:  # Listo
            cocina.horafinalizada = timezone.now().time()

        cocina.save()
        return JsonResponse({"success": True})


def enviar_a_cocina(request):
    body = json.loads(request.body)
    mesaId = body.get("mesaId")
    platoId = body.get("platoId")  
    if not mesaId or not platoId:
        return JsonResponse({"status": "error", "message": "Datos incompletos."}, status=400)
    print(f"Enviando a cocina: Mesa {mesaId}, Plato {platoId}")

    # Crear registro en cocina
    try:
        cocinas = Cocinas(
            mesaid_id=mesaId,
            platoid_id=platoId,
            estado=0,  # Pendiente por defecto
            hora = timezone.now().time(),
        )
        cocinas.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        print(f"Error al enviar a cocina: {e}")
        return JsonResponse({"status": "error"})
    
