import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from restaurante.models import Cajas, Detallefacturaplato, Detallefacturaproducto, Facturas, Lotesproductos, Opciones, Platos, Productos
from restaurante.views import lotes
from ..view import datosUser
from ..utils import login_required
from django.db import transaction
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


def  nueva_Factura_Unica(request):
    user_data = datosUser(request)
    datos = {**user_data}
    
    return render(request, 'pages/cuentas/agregarDelivery.html', datos)


@login_required
def buscar_productos(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        query = request.GET.get("q", "")
        
        data = []

        # Buscar platos
        platos = Platos.objects.filter(nombre__icontains=query, estado=1) if query else Productos.objects.none()
        for plato in platos:
            data.append({
                "tipo": "plato",
                "id": plato.platoid,
                "nombre": plato.nombre,
                "precio": plato.precio,
                "stock": None,  # No aplica
                "descripcion": plato.descripcion or '',
                "categoria": plato.categoriaid.nombre,
                "imagen": static('productos/' + str(plato.rutafoto)) if plato.rutafoto else static('img/defaultImage.png'),
            })
            
        # Buscar productos
        productos = Productos.objects.filter(nombre__icontains=query, estado=1) if query else Productos.objects.none()
        for producto in productos:
            data.append({
                "tipo": "producto",
                "id": producto.productoid,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "stock": producto.stock,
                "descripcion": producto.descripcion or '',
                "categoria": producto.categoriaid.nombre,
                "imagen": static('productos/' + str(producto.rutafoto)) if producto.rutafoto else static('img/defaultImage.png'),
            })

        return JsonResponse({"productos": data})
    
    return JsonResponse({"error": "Peticion invalida"}, status=400)

@csrf_exempt
@transaction.atomic
def guardar_Factura_Unica(request):
    print("Guardando factura única...")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = request.session['user_id']
            productos = data.get('productos', [])
            cliente = data.get('cliente', 'Generico')
            tipo_pago = data.get('tipoPago')
            
            efectivo_corodoba = data.get('efectivo_cordoba', 0)
            efectivo_dolar = data.get('efectivo_dolar', 0)
            
            tasa = Opciones.objects.first()
            tasa_cambio = tasa.tasacambio
            
            caja = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
            
            if not caja:
                return JsonResponse({"success": False, "message": "Abra una caja primero"}, status=400)
            
            factura = Facturas.objects.create(
                fecha=timezone.now(),
                mesaid=None,
                usuarioid_id=usuario_id,
                clientenombre=cliente,
                estado=1,
                cordobas=efectivo_corodoba,
                dolares=efectivo_dolar,
                tasacambio=tasa_cambio,
                tipo=tipo_pago,
                cajaid=caja.cajaid,
            )
            
            for item in productos:
                tipo = item.get('tipo')
                cantidad = item.get('cantidad')
                precio = item.get('precio')
                
                if tipo == 'producto':
                    
                    producto = Productos.objects.get(productoid=item['id'])
                    
                    Detallefacturaproducto.objects.create(
                        facturaid=factura,
                        productoid=producto,
                        cantidad=cantidad,
                        preciounitario=precio,
                    )
                    print("entra")
                    restante = cantidad
                    acti = False
                    while restante > 0:
                        try:
                            lote = Lotesproductos.objects.filter(productoid=producto, estado=1).first()
                            if not lote:
                                lote = Lotesproductos.objects.filter(productoid=producto, estado=3).order_by('loteid').first()
                                if lote:
                                    lote.estado = 1
                                    acti = True
                                else:
                                    raise Exception("No hay suficiente stock disponible")
                                
                            if lote.stock >= restante:
                                lote.stock -= restante
                                producto.stock -= restante
                                if lote.stock == 0:
                                    lote.estado = 2
                                lote.save()
                                restante = 0
                            else:
                                restante -= lote.stock
                                producto.stock -= lote.stock
                                lote.stock = 0
                                lote.estado = 2
                                lote.save()
                        except Lotesproductos.DoesNotExist:
                            raise Exception("No hay lotes disponibles para el producto")
                    if acti:
                        lote = Lotesproductos.objects.filter(productoid=producto, estado=1).first()
                        producto.precio = lote.precioventa
                        
                    producto.save()
                else:
                    plato = Platos.objects.get(platoid=item['id'])
                    
                    Detallefacturaplato.objects.create(
                        facturaid=factura,
                        platoid=plato,
                        cantidad=cantidad,
                        preciounitario=precio,
                    )
                    
            imprimir(factura.facturaid)        
            
            return JsonResponse({"success": True, "message": "Factura guardada correctamente"})
            
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})
        
    return JsonResponse({"success": False, "message": "Método no permitido"})
    


from escpos.printer import Win32Raw
 # para convertir fecha si usas timezone
from PIL import Image

def imprimir(facturaid):
    try:
        printer = Win32Raw("POS-58")

        factura = Facturas.objects.get(facturaid=facturaid)
        detalles_platos = Detallefacturaplato.objects.filter(facturaid=factura)
        detalles_productos = Detallefacturaproducto.objects.filter(facturaid=factura)
        opc = Opciones.objects.first()
        
        logo_path = os.path.join(settings.BASE_DIR, "restaurante/static/image/logo.bmp")
        if os.path.exists(logo_path):
            print("Imprimiendo logo...")
            img = Image.open(logo_path)
            printer.image(img) 
        
        printer.text("RUC: " + opc.numeroruc + "\n")
        printer.text("Telefono: " + opc.telefono + "\n")
        printer.text(f"Factura No: {factura.facturaid}\n")

        printer.text(f"Cliente: {factura.clientenombre}\n")
        
        fecha_local = timezone.now()
        printer.text(f"Fecha: {fecha_local.strftime('%d/%m/%Y %H:%M')}\n")
        printer.text("--------------------------------\n")

        total = 0
        printer.text("Items     Uds    Precio     SubT\n")

        def formato_linea(nombre, cantidad, precio):
            subtotal = cantidad * precio
            # Línea 1: nombre del producto, cortado si es necesario
            linea1 = nombre[:32]

            # Línea 2: concatenar los valores y alinear a la derecha
            cant_str = str(cantidad).rjust(2)
            precio_str = f"C${precio:.2f}"
            subtotal_str = f"C${subtotal:.2f}"
            linea2 = f"{cant_str}   {precio_str}  {subtotal_str}".rjust(32)

            return linea1 + "\n" + linea2

        # Platos
        if detalles_platos.exists():
            for det in detalles_platos:
                nombre = det.platoid.nombre
                cantidad = det.cantidad
                precio = det.preciounitario
                total += cantidad * precio
                printer.text(formato_linea(nombre, cantidad, precio) + "\n")

        # Productos
        if detalles_productos.exists():
            for det in detalles_productos:
                nombre = det.productoid.nombre
                cantidad = det.cantidad
                precio = det.preciounitario
                total += cantidad * precio
                printer.text(formato_linea(nombre, cantidad, precio) + "\n")

        printer.text("--------------------------------\n")
        total_line = f"Total:{f'C${total:.2f}'.rjust(26)}"
        
        tasa_cambio_line = f"Tasa de Cambio: {f'C${factura.tasacambio}':>15}"
        pago_line = f"Pago en Dólares: {f'${factura.dolares:.2f}':>15}"
        pago_line2 = f"Pago en Córdobas:  {f'C${factura.cordobas:.2f}':>13}"
        # Cálculo del cambio
        cambio = float(factura.cordobas) + (float(factura.dolares) * float(factura.tasacambio)) - total
        cambio_line = f"Cambio:   {f'C${cambio:.2f}':>22}"

        # Impresión
        printer.text(total_line + "\n")
        printer.text(tasa_cambio_line + "\n")
        printer.text(pago_line + "\n")
        printer.text(pago_line2 + "\n")
        printer.text(cambio_line + "\n")
        printer.text("--------------------------------\n")
        printer.text(opc.mensaje)
        printer.text("\n\n\n\n\n\n")
        printer.cashdraw(2)
        printer.close()  # Cerrar la impresora
        print("Factura impresa exitosamente.")

    except Exception as e:
        print(f"Error al imprimir la factura: {e}")
