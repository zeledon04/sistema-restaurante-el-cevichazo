import json
from django.http import JsonResponse
from django.shortcuts import render
from restaurante.models import Cuentastemporales, Mesas
from ..view import datosUser
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone

def  agregarCuentas(request, id):
    user_data = datosUser(request)
    print(f"ID de la mesa: {id}")
    cuentas = Cuentastemporales.objects.all().filter(mesaid_id=id, estado=1)
    mesa = Mesas.objects.get(mesaid=id).numero
    print(f"Total de cuentas activas: {cuentas.count()}")
    datos = {**user_data, 'cuentas': cuentas, 'mesa_id': id, 'mesa_numero': mesa}
    return render(request, 'pages/cuentas/agregarCuentas.html', datos)


@csrf_exempt
@transaction.atomic
def crear_cuenta_temporal(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mesaid = data.get("mesaid")
        print(f"ID de la mesa recibida: {mesaid}")
        usuarioid = Mesas.objects.get(mesaid=mesaid).mesero
        clientenombre = data.get("clientenombre")
        print(f"Creando cuenta temporal para la mesa: {mesaid}, usuario: {usuarioid}, cliente: {clientenombre}")
        
        cuenta = Cuentastemporales.objects.create(
            mesaid_id=mesaid,
            usuarioid_id=usuarioid,
            fechacreacion=timezone.now(),
            estado=1,
            clientenombre=clientenombre
        )
        return JsonResponse({"success": True, "cuenta_id": cuenta.cuentatemporalid})
    return JsonResponse({"success": False}, status=400)