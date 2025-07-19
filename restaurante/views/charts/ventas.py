# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.db.models import Sum
from restaurante.models import Historialventas
import json

@csrf_exempt
def datos_grafico(request):
    body = json.loads(request.body)
    modo = body.get('modo')
    hoy = datetime.today().date()

    if modo == 'semana':
        # print("Modo: "+modo)
        # print(f"Hoy: {hoy}")
        inicio = hoy - timedelta(days=hoy.weekday())
        # print(f"Inicio: {inicio}")
        dias = [(inicio + timedelta(days=i)) for i in range(7)]
        # print(f"Días: {dias}")
        labels = [d.strftime('%A') for d in dias]
        # print(f"DíasStr: {labels}")
        datos = [float(Historialventas.objects.filter(fechaventa=d).aggregate(cantidadtotal =Sum('cantidadtotal'))['cantidadtotal'] or 0) for d in dias]
        # print(f"DATOS: {datos}")
        return JsonResponse({'labels': labels, 'datos': datos})

    elif modo == 'mes':
        print("Modo: "+modo)
        meses = []
        datos = []
        for i in range(5, -1, -1):
            # print(i)
            mes = hoy.month - i
            anio = hoy.year
            if mes <= 0:
                mes += 12
                anio -= 1
            # print(f"Mes: {mes}")
            # print(f"Año: {anio}")
                
            inicio = datetime(anio, mes, 1).date()
            # print(f"Inicio: {inicio}")
            fin = datetime(anio + 1, 1, 1).date() if mes == 12 else datetime(anio, mes + 1, 1).date()
            # print(f"Fin: {fin}")
            total = Historialventas.objects.filter(fechaventa__gte=inicio, fechaventa__lt=fin).aggregate(cantidadtotal=Sum('cantidadtotal'))['cantidadtotal'] or 0
            # print(total)
            meses.append(inicio.strftime('%B'))
            datos.append(float(total))
        return JsonResponse({'labels': meses, 'datos': datos})

    elif modo == 'rango':
        print("Modo: "+modo)
        inicio = datetime.strptime(body['inicio'], "%Y-%m-%d").date()
        print(f"Inicio: {inicio}")
        fin = datetime.strptime(body['fin'], "%Y-%m-%d").date()
        print(f"Fin: {fin}")
        dias = []
        datos = []
        actual = inicio
        while actual <= fin:
            dias.append(actual.strftime('%Y-%m-%d'))
            total = Historialventas.objects.filter(fechaventa=actual).aggregate(cantidadtotal=Sum('cantidadtotal'))['cantidadtotal'] or 0
            datos.append(float(total))
            actual += timedelta(days=1)
        return JsonResponse({'labels': dias, 'datos': datos})

    return JsonResponse({'error': 'Modo no válido'}, status=400)
    # return JsonResponse({'status': 'ok', 'modo': modo})
