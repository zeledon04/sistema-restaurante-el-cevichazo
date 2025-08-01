from datetime import date, timedelta
from django.forms import FloatField
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, authenticate
from restaurante.models import Cajas, Cocinas, Detallefacturaplato, Detallefacturaproducto, Facturas, Lotesproductos, Mesas, Opciones, Productos, Usuarios
from django.contrib import messages
from .utils import login_required, logout_required, admin_required, vendedor_required

def notificacion_platos_listos():
    cocinas = Cocinas.objects.filter(estado=1)
    notificaciones = []
    nombreomesa = None
    for cocina in cocinas:
        if not cocina.cliente:
            nombreomesa = "Mesa #" + str(cocina.mesaid.numero)
        else:
            nombreomesa = cocina.cliente
        notificaciones.append({
            'nombreplato': cocina.platoid.nombre,
            'nombreomesa': nombreomesa,  # tipo datetime en la que entro a preparacion se guardo con funcion timezone.now() de la libreria django.utils
        })
        
    return notificaciones
def notificacion_platos_pendientes():
    cocinas = Cocinas.objects.filter(estado=0)
    notificaciones = []
    nombreomesa = None
    for cocina in cocinas:
        if not cocina.cliente:
            nombreomesa = "Mesa #" + str(cocina.mesaid.numero)
        else:
            nombreomesa = cocina.cliente
        notificaciones.append({
            'nombreplato': cocina.platoid.nombre,
            'nombreomesa': nombreomesa,
            'hora': cocina.hora  # tipo datetime en la que entro a preparacion se guardo con funcion timezone.now() de la libreria django.utils
        })
        
        
    return notificaciones

def notificacion_platos_preparacion():
    cocinas = Cocinas.objects.filter(estado=2)
    notificaciones = []
    nombreomesa = None
    for cocina in cocinas:
        if not cocina.cliente:
            nombreomesa = "Mesa #" + str(cocina.mesaid.numero)
        else:
            nombreomesa = cocina.cliente
        notificaciones.append({
            'nombreplato': cocina.platoid.nombre,
            'nombreomesa': nombreomesa,
            'tiempo_estimado': cocina.platoid.tiempo, #tiempo en minutos tipo entero
            'hora': cocina.horapreparacion # tipo datetime en la que entro a preparacion se guardo con funcion timezone.now() de la libreria django.utils
        })
        
    return notificaciones

def notificar_stock_bajo():
    productos_bajos = Productos.objects.filter(stock__lte=30, estado=1)

    notificaciones = []
    
    for producto in productos_bajos:
        notificaciones.append({
            'id': producto.productoid,
            'nombre': producto.nombre,
            'stock': producto.stock
        })
    return notificaciones

def notificar_vencimientos():
    hoy = date.today()
    # 4 meses ≈ 120 días
    limite = hoy + timedelta(days=120)
    proximos_vencimientos = Lotesproductos.objects.filter(fechavencimiento__lte=limite, estado=1)
    
    notificaciones = []
    
    for lote in proximos_vencimientos:
        producto = lote.productoid
        notificaciones.append({
            'id': producto.productoid,
            'nombre': producto.nombre,
            'fecha_vencimiento': lote.fechavencimiento,
            'loteid': lote.loteid
        })
    
    return notificaciones

def datosUser(request):
    platosPreparacion = notificacion_platos_preparacion()
    user = Usuarios.objects.get(pk=request.session['user_id'])
    notisStock = notificar_stock_bajo()
    notisVencimiento = notificar_vencimientos()
    platosPendientes = notificacion_platos_pendientes()
    platosListos = notificacion_platos_listos()
    return {
        'user': user,
        'nombre': user.nombre,
        'userId': user.usuarioid,
        'rolid': user.rol,
        'notisStock': notisStock,
        'notisVencimiento': notisVencimiento,
        'numeroNotificaciones': len(notisVencimiento) + len(notisStock) + len(platosPreparacion) + len(platosPendientes) + len(platosListos),
        'platosPreparacion': platosPreparacion,
        'platosPendientes': platosPendientes,
        'platosListos': platosListos,
    }


# Create your views here.
@login_required
def dashboard(request):
    user_data = datosUser(request)
    caja_abierta = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
    mesas_ocupadas = Mesas.objects.filter(estado=1).count()
    

    if caja_abierta:
        facturas_caja = Facturas.objects.filter(cajaid=str(caja_abierta.cajaid), estado=1)

        detalles = Detallefacturaproducto.objects.filter(facturaid__in=facturas_caja).values('facturaid').annotate(
            total=Sum(ExpressionWrapper(F('cantidad') * F('preciounitario'), output_field=FloatField()))
        )
        totales_detalles = {d['facturaid']: d['total'] for d in detalles}

        detalles_ropa = Detallefacturaplato.objects.filter(facturaid__in=facturas_caja).values('facturaid').annotate(
            total=Sum(ExpressionWrapper(F('cantidad') * F('preciounitario'), output_field=FloatField()))
        )
        totales_ropa = {d['facturaid']: d['total'] for d in detalles_ropa}

        efectivo_cordobas = caja_abierta.cordobasinicial or 0
        efectivo_dolares = caja_abierta.dolaresinicial or 0

        ingresos_cordobas = 0
        total_ventas = 0
        if facturas_caja:
            
            for factura in facturas_caja:
                cordobas_recibidos = factura.cordobas or 0
                dolares_recibidos = factura.dolares or 0
                tasa = factura.tasacambio or 0

                total_factura = totales_detalles.get(factura.facturaid, 0) + totales_ropa.get(factura.facturaid, 0)
                total_pagado_en_cordobas = cordobas_recibidos + dolares_recibidos * float(tasa)
                vuelto = total_pagado_en_cordobas - total_factura

                # Sumamos solo lo que realmente se recibió
                efectivo_cordobas += cordobas_recibidos
                efectivo_dolares += dolares_recibidos

                # Restamos el vuelto en C$
                efectivo_cordobas -= max(vuelto, 0)

                # Ingresos contables (para reportes, no afecta físico)
                ingresos_cordobas += total_factura
                total_ventas = facturas_caja.count()
        else:
            total_ventas = 0
            
    if caja_abierta:
        datos = {
            **user_data,
            'hora': caja_abierta.fechaapertura,
            'tiempo': caja_abierta.fechaapertura,
            'caja': caja_abierta,
            'mesas_ocupadas': mesas_ocupadas,
            'efectivo_cordobas': round(efectivo_cordobas, 2),
            'efectivo_dolares': round(efectivo_dolares, 2),
            'ingresos_cordobas': round(ingresos_cordobas, 2),
            'total_ventas': total_ventas,
            
        }
        return render(request, 'dashboard.html', datos)
    return render(request, 'dashboard.html', user_data)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('pass')
        
        try:
            user = Usuarios.objects.get(user=username)
            
            if check_password(password, user.contra):
                request.session['user_id'] = user.pk
                
                return redirect('dashboard')
            else:
                return render(request, 'auth/login.html', {'error': 'Credenciales inválidas'})
            
        except Usuarios.DoesNotExist:
            return render(request, 'auth/login.html', {'error': 'Usuario no encontrado'})

        
    else:
        return render(request, 'auth/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')


def obtener_tasa_cambio(request):
    try:
        opcion = Opciones.objects.first()
        tasa = opcion.tasacambio if opcion else None
        return JsonResponse({'tasaCambio': tasa})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)