from decimal import Decimal
import json
import pdfkit  # type: ignore
import os
import base64
import shutil
from django.http import HttpResponse , JsonResponse 
from django.conf import settings
from ..models import Usuarios  
from datetime import datetime

from ..utils import admin_required, logout_required, login_required

@admin_required
def registro_ventas_del_dia_pdf(request):

    temp_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'Reportes')
    pdf_file = os.path.join(temp_dir, 'reporte_ventas_del_dia.pdf')
    
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_ventas_del_dia.pdf"'
    return response

def imprimir_registro_ventas_del_dia(request):
    if request.method == 'POST':
        # items_json = request.body.decode('utf-8')
        
        # data = json.loads(items_json)
        # datos = data['items']
        data = json.loads(request.body.decode('utf-8'))
        productos = data.get('productos', [])
        platos = data.get('platos', [])
        datos = []
        for producto in productos:
            datos.append({
                'numero': producto['numero'],
                'producto': producto['producto'],
                'fecha': producto['fecha'],
                'cantidad': producto['cantidad'],
                'precioVenta': producto.get('precioVenta'),
                'subtotal': producto['subtotal'],
                'tipo': 'producto',
                'precioCompra': producto.get('precioCompra')
            })
        for plato in platos:
            datos.append({
                'numero': plato['numero'],
                'producto': plato['producto'],
                'fecha': plato['fecha'],
                'cantidad': plato['cantidad'],
                'precioVenta': plato.get('precioVenta'),
                'subtotal': plato['subtotal'],
                'tipo': 'plato',
                'precioCompra': plato.get('precioCompra', 0.0)
            })
        rutaLogo = settings.LOGO_PATH
        vendedor = Usuarios.objects.get(pk=request.session['user_id'])
        nombreVendedor = f"{vendedor.nombre}"

        generar_registro_ventas_del_dia(productos, platos, rutaLogo, nombreVendedor)

    return JsonResponse({'success': True})

def generar_registro_ventas_del_dia(productos, platos, ruta, nombreVendedor):
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
        <meta charset="UTF-8">
        <title>Historial de Ventas del día</title>
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
            
        <div class="center" style="margin: 0 10px">
            <p style="margin-bottom: 1; padding: 5px; background-color: #047857; color: white; border-radius: 5px; font-size: 14px; font-weight: bold;">
                Ventas del día de Productos
            </p>
        </div>
            
        </div>
        
        <table>
            <tr>
                <th class="p-2">#</th>
                <th class="p-2">Producto</th>
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
    cont = 1
    for data in productos:
        numero = cont
        cont += 1
        producto = data['producto']
        fecha = data['fecha']
        precioCompra = data['precioCompra']
   
        precioVenta = data['precioVenta']
 
        cantidad = data['cantidad']
        subtotal = Decimal(str(data['subtotal']))
        sub = Decimal(str(precioCompra)) * int(cantidad)
        
        ticket_html += f"""
            <tr>
                <td>{numero}</td>
                <td>{producto}</td>
                <td>{fecha}</td>
                <td>{cantidad}</td>
                <td>C$ {Decimal(precioVenta):.2f}</td>
                <td>C$ {subtotal:.2f}</td>
                <td>C$ {Decimal(precioCompra):.2f}</td>
                <td>C$ {sub:.2f}</td>
            </tr>
        """
        totall += subtotal
        totalPrecioCompra += sub

    ticket_html += f"""
            <tr style="background-color: #e2f0d9; font-weight: bold;">
                <td colspan="5">Total</td>
                <td>C$ {totall:.2f}</td>
                <td>----</td>
                <td>C$ {totalPrecioCompra:.2f}</td>
            </tr>
            <tr style="background-color: #d9edf7; font-weight: bold;">
                <td colspan="7">Ganancia</td>
                <td>C$ {(totall - totalPrecioCompra):.2f}</td>
            </tr>
            
        </table>
        
        <div class="footer">
            <p>Generado por: {nombreVendedor}</p>
        </div>
     """  
     
    # Agregar sección de ventas de platos
     
    ticket_html += f"""
        <div class="center" style="margin: 0 10px">
            <p style="margin-bottom: 1; padding: 5px; background-color: #047857; color: white; border-radius: 5px; font-size: 14px; font-weight: bold;">
                Ventas del día de Platos
            </p>
        </div>

        <table>
            <tr>
                <th class="p-2">#</th>
                <th class="p-2">Plato</th>
                <th class="p-2">Fecha</th>
                <th class="p-2">Cantidad</th>
                <th class="p-2">Precio Venta</th>
                <th class="p-2">Subtotal Venta</th>
            </tr>
    """

    totalPlatos = Decimal("0.00")
    cont = 1
    for data in platos:
        numeroPlato = cont
        cont += 1
        productoPlato = data['producto']
        fechaPlato = data['fecha']
        cantidadPlato = data['cantidad']
        precioVentaPlato = data['precioVenta']
        # if precioVentaPlato is None or precioVentaPlato == '':
        #     precioVentaPlato = 0.0
        subtotalPlato = Decimal(str(data['subtotal']))

        ticket_html += f"""
            <tr>
                <td>{numeroPlato}</td>
                <td>{productoPlato}</td>
                <td>{fechaPlato}</td>
                <td>{cantidadPlato}</td>
                <td>C$ {Decimal(precioVentaPlato):.2f}</td>
                <td>C$ {subtotalPlato:.2f}</td>
            </tr>
        """
        totalPlatos += subtotalPlato

    ticket_html += f"""
            <tr style="background-color: #e2f0d9; font-weight: bold;">
                <td colspan="5">Total Platos</td>
                <td>C$ {totalPlatos:.2f}</td>
            </tr>
        </table>
    """

     
    ticket_html += f"""
        
        <div class="footer">
            <p>Generado por: {nombreVendedor}</p>
        </div>
    </body>
    </html>
    """
    nombre_archivo_html = f"reporte_ventas_del_dia_{fecha_actual.strftime('%Y%m%d')}.html"
    nombre_archivo_pdf = f"reporte_ventas_del_dia_{fecha_actual.strftime('%Y%m%d')}.pdf"
    
    # Obtener ruta dinámica al escritorio del usuario
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") # aquí tené cuidado porque la carpeta puede llamarse "Escritorio" en español
    temp_dir = os.path.join(desktop_path, 'Reportes')
    os.makedirs(temp_dir, exist_ok=True)

    # Ruta para HTML y copia PDF fija
    temp_dir_html = os.path.join(os.environ.get('LOCALAPPDATA'), 'Restaurante', 'Reportes')
    os.makedirs(temp_dir_html, exist_ok=True)
    
    
    html_file = os.path.join(temp_dir_html, nombre_archivo_html)
    pdf_file = os.path.join(temp_dir, nombre_archivo_pdf)
    
    # Guardar HTML temporal
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(ticket_html)
        
    # Generar PDF
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_file, pdf_file, configuration=config)
    
    # Copiar PDF generado a ruta fija para abrir en navegador
    pdf_copia_fija = os.path.join(temp_dir_html, 'reporte_ventas_del_dia.pdf')
    shutil.copyfile(pdf_file, pdf_copia_fija)
