import json
from django.http import JsonResponse
from django.shortcuts import render
from restaurante.models import Cuentastemporales, Detallecuentatemporalplato, Detallecuentatemporalproducto, Mesas, Productos, Platos
from ..view import datosUser
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone

from collections import defaultdict
from ..utils import login_required

@login_required
def agregarCuentas(request, id):
    user_data = datosUser(request)
    
    cuentas = Cuentastemporales.objects.filter(mesaid_id=id, estado=1)
    mesa = Mesas.objects.get(mesaid=id).numero

    # Diccionario para guardar los detalles por cuenta
    detalles_por_cuenta = defaultdict(lambda: {'productos': [], 'platos': []})

    for cuenta in cuentas:
        detalles_producto = Detallecuentatemporalproducto.objects.filter(cuentatemporalid=cuenta)
        detalles_plato = Detallecuentatemporalplato.objects.filter(cuentatemporalid=cuenta)
        
        print(cuenta.usuarioid.nombre)
        
        detalles_por_cuenta[cuenta.cuentatemporalid]['productos'] = detalles_producto
        detalles_por_cuenta[cuenta.cuentatemporalid]['platos'] = detalles_plato
    
    totales_por_cuenta = {}

    for cuenta in cuentas:
        cuenta_id = cuenta.cuentatemporalid
        detalles = detalles_por_cuenta.get(cuenta_id, {'platos': [], 'productos': []})

        total = 0
        for plato in detalles['platos']:
            total += plato.cantidad * plato.platoid.precio

        for producto in detalles['productos']:
            total += producto.cantidad * producto.productoid.precio

        totales_por_cuenta[cuenta_id] = total
    
    datos = {
        **user_data,
        'cuentas': cuentas,
        'mesa_id': id,
        'mesa_numero': mesa,
        'detalles_por_cuenta': detalles_por_cuenta,
        'totales_por_cuenta': totales_por_cuenta,
    }
        
    return render(request, 'pages/cuentas/agregarCuentas.html', datos)

@login_required
@csrf_exempt
@transaction.atomic
def crear_cuenta_temporal(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mesaid = data.get("mesaid")
        usuarioid = Mesas.objects.get(mesaid=mesaid).mesero
        clientenombre = data.get("clientenombre")
        
        cuenta = Cuentastemporales.objects.create(
            mesaid_id=mesaid,
            usuarioid_id=usuarioid,
            fechacreacion=timezone.now(),
            estado=1,
            clientenombre=clientenombre
        )
        return JsonResponse({"success": True, "cuenta_id": cuenta.cuentatemporalid})
    return JsonResponse({"success": False}, status=400)

@login_required
@csrf_exempt
@transaction.atomic
def actualizar_cuenta_temporal(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        cuenta_id = data.get('cuentaId')
        detalles = data.get('detalles', [])
        
        platos_a_actualizar = []
        productos_a_actualizar = []

        for item in detalles:
            tipo = item.get('tipo')
            item_id = item.get('id')

            cantidad = item.get('cantidad')

            if tipo == 'plato':
                plato = Platos.objects.get(platoid=item_id)
                detalle, creado = Detallecuentatemporalplato.objects.get_or_create(
                    cuentatemporalid_id=cuenta_id,
                    platoid=plato,
                    defaults={'cantidad': cantidad}
                )
                if not creado:
                    detalle.cantidad = cantidad
                    platos_a_actualizar.append(detalle)
            else:
                producto = Productos.objects.get(productoid=item_id)
                detalle, creado = Detallecuentatemporalproducto.objects.get_or_create(
                    cuentatemporalid_id=cuenta_id,
                    productoid=producto,
                    defaults={'cantidad': cantidad}
                )
                if not creado:
                    detalle.cantidad = cantidad
                    productos_a_actualizar.append(detalle)

        if platos_a_actualizar:
            Detallecuentatemporalplato.objects.bulk_update(platos_a_actualizar, ['cantidad'])
        if productos_a_actualizar:
            Detallecuentatemporalproducto.objects.bulk_update(productos_a_actualizar, ['cantidad'])


        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def eliminar_detalle_cuenta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cuenta_id = data.get('cuenta')
        id = data.get('id')
        tipo = data.get('tipo')

        if tipo == 'plato':
            Detallecuentatemporalplato.objects.filter(cuentatemporalid_id=cuenta_id, platoid__platoid=id).delete()
        else:
            Detallecuentatemporalproducto.objects.filter(cuentatemporalid_id=cuenta_id, productoid__productoid=id).delete()

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def eliminar_cuenta_temporal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')

        try:
            cuenta = Cuentastemporales.objects.get(cuentatemporalid=id)
            cuentas = Cuentastemporales.objects.filter(mesaid_id=cuenta.mesaid_id, estado=1).count()
            if cuentas == 1:
                mesa = Mesas.objects.filter(mesaid=cuenta.mesaid_id).first()
                mesa.estado = 0
                mesa.save()
                return JsonResponse({'success': True, 'message': '1'})
            cuenta.delete()
            return JsonResponse({'success': True})
        except Cuentastemporales.DoesNotExist:
            return JsonResponse({'error': 'Cuenta no encontrada'}, status=404)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

from escpos.printer import Win32Raw

@login_required
@csrf_exempt
def imprimir_precuenta(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body)
            platos = datos.get("platos", [])
            total = float(datos.get("total"))  # Puedes enviar esto desde el frontend
            printer = Win32Raw("POS")
            # Encabezado
            printer.set(align='center', width=2, height=2)
            printer.text("\nPRE-CUENTA\n")
            printer.set(align='left')
            printer.text("--------------------------------\n")
            printer.text("Items     Uds    Precio     SubT\n")

            def formato_linea(nombre, cantidad, precio, subtotal):
                linea1 = nombre[:32]
            
                linea2 = f"{str(cantidad).rjust(2)}   C${precio:.2f}  C${subtotal:.2f}".rjust(32)
                return linea1 + "\n" + linea2
            # Platos
            for item in platos:
                nombre = item.get("nombre")
                cantidad = int(item.get("cantidad"))
                precio = float(item.get("precio"))
                subtotal = float(item.get("subtotal"))
                printer.text(formato_linea(nombre, cantidad, precio, subtotal) + "\n")

            printer.text("--------------------------------\n")
            total_line = f"Total:{f'C${total:.2f}'.rjust(26)}"
            printer.text(total_line + "\n")
            printer.text("\nGracias por su preferencia\n")
            printer.text("\n\n\n\n")
            printer.close()

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)


