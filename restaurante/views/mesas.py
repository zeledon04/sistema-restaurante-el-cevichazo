from datetime import datetime
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone

from restaurante.models import Cuentastemporales, Mesas, Usuarios
from ..view import datosUser

# Create your views here.
def listarMesas(request):
    user_data = datosUser(request)

    # Obtener todas las mesas ocupadas (estado=1)
    mesas_ocupadas = Mesas.objects.filter(estado=1)

    # Obtener todas las cuentas activas relacionadas a esas mesas
    cuentas = Cuentastemporales.objects.filter(mesaid__in=mesas_ocupadas, estado=1)

    mesas_dict = {}  # clave: mesaid, valor: cuenta representativa
    cont = 0

    for cuenta in cuentas:
        mesa_id = cuenta.mesaid.mesaid
        if mesa_id not in mesas_dict:
            mesas_dict[mesa_id] = cuenta
            cont += 1  # contar solo una vez por mesa

    mesas = []
    for cuenta in mesas_dict.values():
        mesa = cuenta.mesaid
        mesero_nombre = cuenta.usuarioid.nombre if cuenta.usuarioid else "Sin mesero"
        mesas.append({
            'mesa_id': mesa.mesaid,
            'numero': mesa.numero,
            'cliente': cuenta.clientenombre,
            'mesero': mesero_nombre,
            'hora': mesa.fecha,
        })

    return render(request, 'pages/mesas/listarMesas.html', {
        **user_data,
        'mesas': mesas,
        'numMesas': cont
    })

@transaction.atomic
def agregarMesa(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        numero = data.get('numero')
        mesero_id = data.get('mesero')
        cliente = data.get('cliente')

        if not numero or not mesero_id or not cliente:
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

        try:
            # Crear mesa
            nueva_mesa = Mesas(numero=numero, mesero=mesero_id, estado=1, fecha=timezone.now())
            nueva_mesa.save()

            # Crear cuenta temporal (factura temporal)
            mesero = Usuarios.objects.get(pk=mesero_id)
            cuenta = Cuentastemporales(
                mesaid=nueva_mesa,
                usuarioid=mesero,
                fechacreacion=timezone.now(),
                estado=1,  # estado abierta
                clientenombre=cliente
            )
            cuenta.save()

            return JsonResponse({'message': 'Mesa creada exitosamente'})
        
        except Exception as e:
            return JsonResponse({'error': f'Error al guardar: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_meseros(request):
    meseros = Usuarios.objects.filter(rol=2).values('usuarioid', 'nombre')
    return JsonResponse(list(meseros), safe=False)