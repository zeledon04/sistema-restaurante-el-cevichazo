import json
import pdfkit  # type: ignore
import base64
import os
from django.http import HttpResponse , JsonResponse 
from django.core.paginator import Paginator
from django.conf import settings
from ..models import Usuarios, Facturas, Detallefacturaplato, Detallefacturaproducto, Cajas, Lotesproductos
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from ..view import datosUser
from ..utils import admin_required, login_required
from django.db.models import Q
from datetime import timedelta

@login_required
def historialFacturacion(request):
    user_data = datosUser(request)

    if user_data["rolid"] == 1:
        facturas_queryset = Facturas.objects.filter(estado=1).order_by('-facturaid')
    else:
        facturas_queryset = Facturas.objects.filter(estado=1, usuarioid=user_data['userId']).order_by('-facturaid')
    paginator = Paginator(facturas_queryset, 50)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    cont = (page_obj.number - 1) * paginator.per_page + 1
    for factura in page_obj:
        
        cant_producto = Detallefacturaproducto.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        
        cant_platos = Detallefacturaplato.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        
        factura.cantProductos = cant_producto + cant_platos

        total_producto = Detallefacturaproducto.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('preciounitario') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0

        total_platos = Detallefacturaplato.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('preciounitario') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0

        factura.total = total_producto + total_platos
        factura.cont = cont
        cont += 1

    datos = {**user_data, 'facturas': page_obj, 'usuarios': Usuarios.objects.all()}
    return render(request, 'pages/facturas/historial.html', datos)


@login_required
def detalle_factura_json(request, factura_id):
    factura = Facturas.objects.get(pk=factura_id)

    detalles_prod = Detallefacturaproducto.objects.filter(facturaid=factura)
    detalles_plat = Detallefacturaplato.objects.filter(facturaid=factura)

    productos = [{
        'nombre': d.productoid.nombre,
        'cantidad': d.cantidad,
        'precio': float(d.preciounitario),
        'subtotal': float(d.cantidad * d.preciounitario),
    } for d in detalles_prod]

    platos = [{
        'nombre': d.platoid.nombre,
        'cantidad': d.cantidad,
        'precio': float(d.preciounitario),
        'subtotal': float(d.cantidad * d.preciounitario),
    } for d in detalles_plat]

    total = sum(p['subtotal'] for p in productos + platos)
    tasa = float(factura.tasacambio)
    efectivo_cordobas = float(factura.cordobas)
    efectivo_dolares = float(factura.dolares)

    total_entregado = efectivo_cordobas + (efectivo_dolares * tasa)
    cambio = round(total_entregado - total, 2) if total_entregado > total else 0.0

    return JsonResponse({
        'cliente': factura.clientenombre,
        'fecha': factura.fecha.strftime("%d/%m/%Y %I:%M %p"),
        'nofactura': factura.facturaid,
        'productos': productos,
        'platos': platos,
        'total': total,
        'tasacambio': tasa,
        'efectivocordobas': efectivo_cordobas,
        'efectivodolares': efectivo_dolares,
        'cambio': cambio,
        'tipopago': factura.tipo  # Agregamos el tipo de pago
    })
    
    
@login_required
def anularFactura(request, facturaid):
    factura = Facturas.objects.get(pk=facturaid)
    caja = Cajas.objects.get(cajaid=factura.cajaid)
    if caja.estado == 0:
        messages.warning(request, "La caja de esta factura ha sido cerrada. No se puede anular")
        return redirect('historial_facturas')
    else:
        # Anular la factura
        factura.estado = 0
        factura.save()

        # Detalles de productos farmacia
        detalles_producto = Detallefacturaproducto.objects.filter(facturaid=factura, estado=1)
        for detalle in detalles_producto:
            producto = detalle.productoid
            cantidad = detalle.cantidad

            # Lote activo para ese producto
            lote = Lotesproductos.objects.filter(productoid=producto, estado=1).first()
            if lote:
                lote.stock += cantidad
                lote.save()

            producto.stock += cantidad
            
            producto.save()

            detalle.estado = 0
            detalle.save()

        # Detalles de productos ropa
        detalles_platos = Detallefacturaplato.objects.filter(facturaid=factura, estado=1)
        for detalle in detalles_platos:
            producto_plato = detalle.platoid
            producto_plato.save()

            detalle.estado = 0
            detalle.save()
        messages.success(request, "Factura " + str(factura.facturaid) + " Anulada Correctamente.")
        return redirect('historial_facturas')
    
 
@login_required  
def filtrar_facturas(request):
    usuario_id = request.GET.get('usuario_id')
    filtro_fecha = request.GET.get('filtro_fecha')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    facturas = Facturas.objects.filter(estado=1)

    if usuario_id:
        facturas = facturas.filter(usuarioid__usuarioid=usuario_id).order_by('-facturaid')

    if filtro_fecha:
        hoy = datetime.today().date()
        if filtro_fecha == 'hoy':
            facturas = facturas.filter(fecha__date=hoy).order_by('-facturaid')
        elif filtro_fecha == 'semana':
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = inicio_semana + timedelta(days=6)
            facturas = facturas.filter(fecha__date__range=[inicio_semana, fin_semana]).order_by('-facturaid')
        elif filtro_fecha == 'mes':
            facturas = facturas.filter(fecha__year=hoy.year, fecha__month=hoy.month).order_by('-facturaid')
        elif filtro_fecha == 'anio':
            facturas = facturas.filter(fecha__year=hoy.year).order_by('-facturaid')
        elif filtro_fecha == 'rango' and fecha_inicio and fecha_fin:
            facturas = facturas.filter(fecha__date__range=[fecha_inicio, fecha_fin]).order_by('-facturaid')

    resultados = []
    for factura in facturas:
        cant_producto = Detallefacturaproducto.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        cant_plato = Detallefacturaplato.objects.filter(facturaid=factura).aggregate(total=Sum('cantidad'))['total'] or 0
        total_producto = Detallefacturaproducto.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('preciounitario') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0
        total_plato = Detallefacturaplato.objects.filter(facturaid=factura).annotate(
            total_linea=ExpressionWrapper(F('preciounitario') * F('cantidad'), output_field=FloatField())
        ).aggregate(total=Sum('total_linea'))['total'] or 0

        resultados.append({
            'facturaid': factura.facturaid,
            'usuario': factura.usuarioid.nombre,
            'cliente': factura.clientenombre,
            'fecha': factura.fecha.strftime('%d/%m/%Y'),
            'hora': factura.fecha.strftime('%H:%M'),
            'cantProductos': cant_producto + cant_plato,
            'total': round(total_producto + total_plato, 2),
        })

    return JsonResponse({'facturas': resultados})
    

@admin_required
def registro_factura_pdf(request):
    
    temp_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'tmp')
    pdf_file = os.path.join(temp_dir, 'registro_facturas.pdf')
    
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="registro_facturas.pdf"'
    return response


def imprimir_registro_facturas(request):
    if request.method == 'POST':
        items_json = request.body.decode('utf-8')
        
        data = json.loads(items_json)
        datos = data['items']
        rutaLogo = settings.LOGO_PATH
        vendedor = Usuarios.objects.get(pk=request.session['user_id'])
        nombreVendedor = f"{vendedor.nombre}"

        generar_registro_facturas(datos, rutaLogo, nombreVendedor)

    return JsonResponse({'success': True})

def generar_registro_facturas(datos, ruta, nombreVendedor):
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    logo_base64 = image_to_base64(ruta)

    fecha_actual = datetime.now()

    dias_semana = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    dia_semana = dias_semana[fecha_actual.strftime("%A")]
    fecha_formateada = f"{dia_semana} {fecha_actual.strftime('%d/%m/%Y %I:%M %p').lower()}"

    ticket_html = f"""
    <html>
    <head>
        <title>Historial de Facturas</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f9; border-radius: 10px;}}
            .center {{ text-align: center;}}
            #logo {{ width: 220px; height: auto; margin-bottom: 10px; padding-top: 20px; }}
            table {{ width: 90%; margin: 20px auto; border-collapse: collapse; box-shadow: 0 2px 3px rgba(0,0,0,0.1); border-radius: 7px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; text-align: left; padding: 8px; font-size: 12px; }}
            th {{ background-color: #047857; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .footer {{ text-align: center; margin-top: 20px; }}
            .footer p {{ font-size: 14px; color: #333; }}
        </style>
    </head>
    <body>
        <div class="center">
            <img id="logo" src="data:image/png;base64,{logo_base64}" alt="Logo">
            <p style="margin-bottom: 1; margin-top: 10px; font-size: 14px; font-weight: bold;">Restaurante El Cevichazo</p>
            <p style="margin-bottom: 1; margin-top: 10px; font-size: 14px; font-weight: bold;"><i>¡El sabor que me gusta!</i></p>
            <p style="margin: 1; font-size: 10px;">{fecha_formateada}</p>
            <p>Historial de Facturas</p>
        </div>

        <table>
            <tr>
                <th class="p-2">#</th>
                <th class="p-2">No.Factura</th>
                <th class="p-2">Vendedor</th>
                <th class="p-2">Cliente</th>
                <th class="p-2">Fecha</th>
                <th class="p-2">Hora</th>
                <th class="p-2">Cant.Productos</th>
                <th class="p-2">Subtotal</th>
            </tr>
    """
    totall = 0
    for data in datos:
        numero = data['numero']
        numFactura = data['numFactura']
        vendedor = data['vendedor']
        cliente = data['cliente']
        fecha = data['fecha']
        hora = data['hora']
        productos = data['productos']
        subtotal = float(data['subtotal'])

        ticket_html += f"""
            <tr>
                <td>{numero}</td>
                <td>{numFactura}</td>
                <td>{vendedor}</td>
                <td>{cliente}</td>
                <td>{fecha}</td>
                <td>C$ {hora}</td>
                <td>{productos}</td>
                <td>C$ {subtotal}</td>
            </tr>
        """
        totall += subtotal

    ticket_html += f"""
            <tr>
                <td colspan="7">Total</td>
                <td>C$ {totall}</td>
            </tr>
        </table>
        <div class="footer">
            <p>Generado por: {nombreVendedor}</p>
        </div>
    </body>
    </html>
    """
    temp_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'tmp')
    os.makedirs(temp_dir, exist_ok=True)
    
    html_file = os.path.join(temp_dir, 'registroTempoFacturas.html')
    pdf_file = os.path.join(temp_dir, 'registro_facturas.pdf')
    
    with open(html_file, "w") as f:
        f.write(ticket_html)
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_file, pdf_file, configuration=config)

