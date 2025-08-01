from decimal import Decimal
import json
import pdfkit  # type: ignore
import os
import base64
from django.http import HttpResponse , JsonResponse 
from django.conf import settings
from ..models import Usuarios  
from datetime import datetime

from ..utils import admin_required, logout_required, login_required

@admin_required
def registro_ventas_pdf(request):
    temp_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'tmp')
    pdf_file = os.path.join(temp_dir, 'registro_ventas.pdf')
    
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="registro_ventas.pdf"'
    return response

def imprimir_registro_ventas(request):
    if request.method == 'POST':
        items_json = request.body.decode('utf-8')
        
        data = json.loads(items_json)
        datos = data['items']
        rutaLogo = settings.LOGO_PATH
        vendedor = Usuarios.objects.get(pk=request.session['user_id'])
        nombreVendedor = f"{vendedor.nombre}"

        generar_registro_facturas(datos, rutaLogo,nombreVendedor)

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
        <title>Historial de Ventas</title>
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
            <p>Historial de Ventas</p>
        </div>

        <table>
            <tr>
                <th class="p-2">#</th>
                <th class="p-2">Tipo</th>
                <th class="p-2">Nombre</th>
                <th class="p-2">Fecha</th>
                <th class="p-2">Cantidad</th>
                <th class="p-2">Precio Venta</th>
                <th class="p-2">SubtotalVenta</th>
                <th class="p-2">Precio Compra</th>
                <th class="p-2">SubtotalCompra</th>

            </tr>
    """
    totall = 0
    totalPrecioCompra = 0
    
    for data in datos:
        numero = data['numero']
        tipo = data.get('tipo', 'Producto')  # Por si acaso falta el campo
        producto = data['producto']
        fecha = data['fecha']
        cantidad = data['cantidad']
        precioVenta = data['precioVenta']
        subtotal = Decimal(str(data['subtotal']))
        precioCompra = data.get('precioCompra')
        if precioCompra is None or precioCompra == '':
            precioCompra_str = '--'
            sub_str = '--'
            sub = Decimal('0')  # No se suma a totalPrecioCompra
        else:
            precioCompra = Decimal(str(data.get('precioCompra')))
            sub = precioCompra * int(cantidad)
            precioCompra_str = f"C$ {precioCompra:.2f}"
            sub_str = f"C$ {sub:.2f}"
            totalPrecioCompra += sub
        
        ticket_html += f"""
            <tr>
                <td>{numero}</td>
                <td>{tipo}</td>
                <td>{producto}</td>
                <td>{fecha}</td>
                <td>{cantidad}</td>
                <td>C$ {Decimal(precioVenta):.2f}</td>
                <td>C$ {subtotal:.2f}</td>
                <td>C$ {precioCompra_str}</td>
                <td>C$ {sub_str}</td>
            </tr>
        """
        totall += subtotal

    ticket_html += f"""
            <tr style="background-color: #e2f0d9; font-weight: bold;">
                <td colspan="6">Total</td>
                <td>C$ {totall:.2f}</td>
                <td>----</td>
                <td>C$ {totalPrecioCompra:.2f}</td>
            </tr>
            <tr style="background-color: #d9edf7; font-weight: bold;">
                <td colspan="8">Ganancia</td>
                <td>C$ {(totall - totalPrecioCompra):.2f}</td>
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
    html_file = os.path.join(temp_dir, 'registroTempoVentas.html')
    pdf_file = os.path.join(temp_dir, 'registro_ventas.pdf')
    
    with open(html_file, "w") as f:
        f.write(ticket_html)
        
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_file, pdf_file, configuration=config)










