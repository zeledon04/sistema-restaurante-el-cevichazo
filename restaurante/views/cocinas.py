from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Mesas, Cocinas, Platos
from django.http import JsonResponse
from ..view import datosUser
from django.views.decorators.csrf import csrf_exempt
from ..utils import login_required
from datetime import datetime
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
    cocinas = Cocinas.objects.filter(estado=0)
    for cocina in cocinas:
        datos.append({
            "cocinaid": cocina.cocinaid,
            "plato": cocina.platoid.nombre,
            "imagen": static('productos/' + str(cocina.platoid.rutafoto)) if cocina.platoid.rutafoto else static('img/defaultImage.png'),
            "hora": cocina.hora,
            "estado": cocina.estado,    
            "mesa": cocina.mesaid.numero if cocina.mesaid else None,
        })
        
    return JsonResponse({"datos":datos})

def enviar_a_cocina(request):
    body = json.loads(request.body)
    mesaId = body.get("mesaId")
    platoId = body.get("platoId")  
    if not mesaId or not platoId:
        return JsonResponse({"status": "error", "message": "Datos incompletos."}, status=400)
    print(f"Enviando a cocina: Mesa {mesaId}, Plato {platoId}")
    # mesaId = request.POST.get("mesaId")
    # platoId = request.POST.get("platoId")

    # Crear registro en cocina
    try:
        cocinas = Cocinas(
            mesaid_id=mesaId,
            platoid_id=platoId,
            estado=0,  # Pendiente por defecto
            hora = datetime.now().strftime("%H:%M")
        )
        cocinas.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        print(f"Error al enviar a cocina: {e}")
        return JsonResponse({"status": "error"})