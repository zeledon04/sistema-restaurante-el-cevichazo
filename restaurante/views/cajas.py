from decimal import Decimal
from django.shortcuts import get_object_or_404, render
import os
from django.conf import settings
# Create your views here.
from django.http import JsonResponse
from restaurante.models import Cajas, Denominacionescaja, Detallefacturaproducto, Detallefacturaplato, Facturas, Lotesproductos, Opciones, Productos, Usuarios
import json
from django.utils import timezone
from django.db import transaction
from restaurante.view import datosUser

from ..utils import admin_required, login_required
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.core.paginator import Paginator
from datetime import  datetime
from django.http import JsonResponse
from django.utils.timezone import now

from ..view import datosUser

@login_required
def verificar_caja(request):
    caja_abierta = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
    if caja_abierta:
        return JsonResponse({'estado': 'abierta', 'hora_apertura': caja_abierta.fechaapertura.strftime('%Y-%m-%d %H:%M:%S')})
    else:
        return JsonResponse({'estado': 'cerrada'})

@transaction.atomic
@login_required
def abrir_caja(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            billetes = data.get("billetes", [])

            # Verificar si ya hay una caja abierta
            ya_abierta = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).exists()
            if ya_abierta:
                return JsonResponse({'error': 'Ya hay una caja abierta.'})

            # Calcular totales
            total_cordobas = sum(b["denominacion"] * b["cantidad"] for b in billetes if b["tipo"] == "cordobas")
            total_dolares = sum(b["denominacion"] * b["cantidad"] for b in billetes if b["tipo"] == "dolares")

            # Crear caja
            apertura = Cajas.objects.create(
                estado=1,
                usuarioid_id=request.session['user_id'],
                fechaapertura=timezone.now(),
                cordobasinicial=total_cordobas,
                dolaresinicial=total_dolares
            )

            # Guardar cada denominación
            for b in billetes:
                Denominacionescaja.objects.create(
                    cajaid=apertura,
                    tipodenominacion=1 if b["tipo"] == "cordobas" else 2,
                    denominacion=b["denominacion"],
                    cantidad=b["cantidad"],
                    tipomovimiento=1,  # Apertura
                    estado=1
                )

            return JsonResponse({
                'success': True,
                'hora_apertura': apertura.fechaapertura.strftime('%H:%M:%S')
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@admin_required
def listarCajas(request):
    user_data = datosUser(request)
    return render(request, 'pages/cajas/listarCajas.html', user_data)

"""
@login_required
def cerrar_caja(request):
    if request.method == 'POST':
        caja = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
        if not caja:
            return JsonResponse({'error': 'No hay una caja abierta.'})

        try:
            data = json.loads(request.body)
            billetes = data.get('billetes', [])

            # Calcular totales
            total_cordobas = sum(b["denominacion"] * b["cantidad"] for b in billetes if b["tipo"] == "cordobas")
            total_dolares = sum(b["denominacion"] * b["cantidad"] for b in billetes if b["tipo"] == "dolares")

            # Guardar denominaciones con tipomovimiento = 2 (cierre)
            for b in billetes:
                Denominacionescaja.objects.create(
                    cajaid=caja,
                    tipodenominacion=1 if b["tipo"] == "cordobas" else 2,
                    denominacion=b["denominacion"],
                    cantidad=b["cantidad"],
                    tipomovimiento=2,  # Cierre
                    estado=1
                )

            # Obtener tasa de cambio
            tasa = Opciones.objects.first()
            tasa_dolar = tasa.tasacambio

            # Calcular ingresos por facturas
            totalingresos = Decimal('0')
            facturas = Facturas.objects.filter(cajaid=caja.cajaid, usuarioid=request.session['user_id'], estado=1)

            for factura in facturas:
                subtotal_productos = Detallefacturas.objects.filter(facturaid=factura, estado=1).aggregate(
                    total=Sum(ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField()))
                )['total'] or 0

                subtotal_ropa = Detallefacturasropa.objects.filter(facturaid=factura, estado=1).aggregate(
                    total=Sum(ExpressionWrapper(F('precio') * F('cantidad'), output_field=FloatField()))
                )['total'] or 0

                total_factura = Decimal(subtotal_productos) + Decimal(subtotal_ropa)
                totalingresos += total_factura

            # Actualizar datos de caja
            caja.estado = 0
            caja.cordobasfinal = total_cordobas
            caja.dolaresfinal = total_dolares
            caja.totalingresos = totalingresos

            sobron = (total_cordobas + (total_dolares * tasa_dolar)) - (
                caja.cordobasinicial + (caja.dolaresinicial * tasa_dolar) + float(totalingresos)
            )

            if sobron > 0:
                caja.sobrante = sobron
                caja.faltante = 0
            elif sobron < 0:
                caja.sobrante = 0
                caja.faltante = abs(sobron)
            else:
                caja.sobrante = 0
                caja.faltante = 0

            caja.fechaciere = now()
            caja.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@admin_required
def listarCajas(request):
    user_data = datosUser(request)
    
    cajas_queryset = Cajas.objects.exclude(estado=1).order_by('-cajaid')
    paginator =  Paginator(cajas_queryset, 50)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for producto in page_obj:
        producto.cont = cont
        cont += 1
    
    datos = {**user_data, 'cajas': page_obj, 'usuarios': Usuarios.objects.all()}
    return render(request, 'pages/cajas/listarCajas.html', datos)

@admin_required
def detalleCaja(request, cajaid):
    user_data = datosUser(request)
    caja = get_object_or_404(Cajas, pk=cajaid)

    denominaciones_apertura = Denominacionescaja.objects.filter(cajaid=caja, tipomovimiento=1)
    denominaciones_cierre = Denominacionescaja.objects.filter(cajaid=caja, tipomovimiento=2)

    def preparar_datos(denominaciones, tipo):
        items = []
        total = 0
        for d in denominaciones:
            if d.tipodenominacion == tipo:
                subtotal = d.denominacion * d.cantidad
                total += subtotal
                items.append({
                    'valor': d.denominacion,
                    'cantidad': d.cantidad,
                    'subtotal': subtotal
                })
        return items, total

    apertura_cordobas, total_apertura_cordobas = preparar_datos(denominaciones_apertura, 1)
    apertura_dolares, total_apertura_dolares = preparar_datos(denominaciones_apertura, 2)
    cierre_cordobas, total_cierre_cordobas = preparar_datos(denominaciones_cierre, 1)
    cierre_dolares, total_cierre_dolares = preparar_datos(denominaciones_cierre, 2)

    datos = {
        **user_data,
        'caja': caja,
        'apertura_cordobas': apertura_cordobas,
        'apertura_dolares': apertura_dolares,
        'cierre_cordobas': cierre_cordobas,
        'cierre_dolares': cierre_dolares,
        'total_apertura_cordobas': total_apertura_cordobas,
        'total_apertura_dolares': total_apertura_dolares,
        'total_cierre_cordobas': total_cierre_cordobas,
        'total_cierre_dolares': total_cierre_dolares
    }

    return render(request, 'pages/cajas/detalleCaja.html', datos)
"""