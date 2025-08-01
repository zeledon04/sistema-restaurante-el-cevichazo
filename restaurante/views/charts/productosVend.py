from django.db.models import Sum
from django.http import JsonResponse
from ...models import Historialventas
from itertools import chain
from django.db.models import F


def productos_mas_vendidos(request):
    labels = []
    datos = []
    
    top_productos = (
        Historialventas.objects
        .filter(productoid__isnull=False)
        .values(nombre=F('productoid__nombre'))
        .annotate(total=Sum('cantidadtotal'))
    )

    top_platos = (
        Historialventas.objects
        .filter(platoid__isnull=False)
        .values(nombre=F('platoid__nombre'))
        .annotate(total=Sum('cantidadtotal'))
    )

    # Convertir a listas de diccionarios con un campo común
    productos = list(top_productos)
    platos = list(top_platos)

    # Combinar y ordenar por total
    top_combinado = sorted(
        chain(productos, platos),
        key=lambda x: x['total'],
        reverse=True
    )[:10]  # Top 10 global

    # print("Datos:")
    for top in top_combinado:
        labels.append(top['nombre'])
        datos.append(top['total'])
    
    return JsonResponse({'labels':labels, 'datos': datos})

