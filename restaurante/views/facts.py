import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from restaurante.models import Cajas, Cuentastemporales, Detallefacturaplato, Detallefacturaproducto, Facturas, Historialventas, Lotesproductos, Mesas, Opciones, Platos, Productos
from restaurante.views import lotes
from ..view import datosUser
from ..utils import login_required
from django.db import transaction
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


@login_required
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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = request.session['user_id']
            productos = data.get('productos', [])
            cliente = data.get('cliente', 'Generico')
            tipo_pago = data.get('tipoPago')
            cuentaSeleccionada = data.get('cuenta_id', None)
            
            mesaId = None
            
            if cuentaSeleccionada:
                cuenta = Cuentastemporales.objects.filter(cuentatemporalid=cuentaSeleccionada, estado=1).first()
                mesaId = cuenta.mesaid
            
            
            
            efectivo_corodoba = data.get('efectivo_cordoba', 0)
            efectivo_dolar = data.get('efectivo_dolar', 0)
            
            referencia = None
            if tipo_pago == '4':
                referencia = efectivo_corodoba
                efectivo_corodoba = 0
            
            tasa = Opciones.objects.first()
            tasa_cambio = tasa.tasacambio
            
            caja = Cajas.objects.filter(usuarioid=request.session['user_id'], estado=1).first()
            
            if not caja:
                return JsonResponse({"success": False, "message": "Abra una caja primero"}, status=400)
            
            factura = Facturas.objects.create(
                fecha=timezone.now(),
                mesaid=mesaId if mesaId else None,
                usuarioid_id=usuario_id,
                clientenombre=cliente,
                estado=1,
                cordobas=efectivo_corodoba,
                dolares=efectivo_dolar,
                tasacambio=tasa_cambio,
                tipo=tipo_pago,
                cajaid=caja.cajaid,
                numref=referencia if referencia else None,
            )
            
            for item in productos:
                tipo = item.get('tipo')
                cantidad = item.get('cantidad')
                precio = item.get('precio')
                
                if tipo == 'producto':
                    
                    producto = Productos.objects.get(productoid=item['id'])
                    lot = Lotesproductos.objects.filter(productoid=producto, estado=1).first()
                    
                    Detallefacturaproducto.objects.create(
                        facturaid=factura,
                        productoid=producto,
                        cantidad=cantidad,
                        preciounitario=precio,
                        estado=1,
                        preciocompra=lot.preciocompraunitario,
                    )
                    
                    Historialventas.objects.create(
                        productoid=producto,
                        cantidadtotal=cantidad,
                        fechaventa=timezone.now(),
                    )
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
                        estado=1
                    )
                    Historialventas.objects.create(
                        platoid=plato,
                        cantidadtotal=cantidad,
                        fechaventa=timezone.now(),
                    )
                    
            imprimir(factura.facturaid, 0)        
            
            cerrar_mesa = None
            if cuentaSeleccionada:
                cuentaSeleccionada = Cuentastemporales.objects.filter(cuentatemporalid=cuentaSeleccionada).first()
                cuentaSeleccionada.estado = 0
                cuentaSeleccionada.save()
                
                mesa_id = cuentaSeleccionada.mesaid_id  # O cuentaSeleccionada.mesaid.pk si quieres ser explícito

                # Buscamos si existen cuentas con estado distinto a 0 (aún abiertas)
                cuentas_abiertas = Cuentastemporales.objects.filter(mesaid=mesa_id).exclude(estado=0)
                
                cerrar_mesa = None
                if not cuentas_abiertas.exists():
                    # Si no hay cuentas abiertas, cerramos la mesa
                    mesa = Mesas.objects.filter(mesaid=mesa_id).first()
                    if mesa:
                        mesa.estado = 0
                        cerrar_mesa = 1
                        mesa.save()
                            
            return JsonResponse({"success": True, "message": "Factura guardada correctamente", "CerrarMesa": cerrar_mesa})
            
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Errffor: {str(e)}"})
        
    return JsonResponse({"success": False, "message": "Método no permitido"})
    


from escpos.printer import Win32Raw
 # para convertir fecha si usas timezone
from PIL import Image

def imprimir_factura(request, facturaid):
    if request.method == 'POST': # 0 para original, 1 para copia
        imprimir(facturaid, 1)
        return JsonResponse({"success": True, "message": "Factura enviada a la impresora"})
    return JsonResponse({"success": False, "message": "Método no permitido"})

def imprimir(facturaid, tipo):
    try:
        factura = Facturas.objects.get(facturaid=facturaid)
        detalles_platos = Detallefacturaplato.objects.filter(facturaid=factura)
        detalles_productos = Detallefacturaproducto.objects.filter(facturaid=factura)
        opc = Opciones.objects.first()
        printer = Win32Raw(opc.nombreimpresora) 
        logo_path = os.path.join(settings.BASE_DIR, "restaurante/static/image/logo.bmp")
        if os.path.exists(logo_path):

            img = Image.open(logo_path)
            
            printer.set(align='center', width=2, height=2)
            max_width = 300  # Ancho máximo en píxeles para la impresora
            w_percent = (max_width / float(img.size[0]))
            new_height = int((float(img.size[1]) * float(w_percent)))

            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
            printer.image(img) 

        
        printer.text("RUC: " + opc.numeroruc + "\n")
        printer.text("Telefono: " + opc.telefono + "\n")
        printer.text(f"Factura No: {factura.facturaid}\n")

        printer.text(f"Cliente: {factura.clientenombre}\n")
        
        if tipo == 1:
            printer.text("Fecha: " + factura.fecha.strftime('%d/%m/%Y %H:%M') + "\n")
        else:
            fecha_local = timezone.now()
            printer.text(f"Fecha: {fecha_local.strftime('%d/%m/%Y %H:%M')}\n")
        if tipo == 1:
            printer.text("Copia\n")
        printer.set(align='left')
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

        tasa_cambio_line = f"Tasa de Cambio: {f'C${float(factura.tasacambio):.2f}':>16}"
        pago_line = f"Pago en Dólares: {f'${factura.dolares:.2f}':>15}"
        pago_line2 = f"Pago en Córdobas:  {f'C${factura.cordobas:.2f}':>13}"
        # Cálculo del cambio
        if factura.tipo == 4:
            cambio_line = "Pago Con Tarjeta"
        else:
            cambio = float(factura.cordobas) + (float(factura.dolares) * float(factura.tasacambio)) - total
            cambio_line = f"Cambio:   {f'C${cambio:.2f}':>22}"

        # Impresión
        printer.text(total_line + "\n")
        printer.text(tasa_cambio_line + "\n")
        printer.text(pago_line + "\n")
        printer.text(pago_line2 + "\n")
        printer.text(cambio_line + "\n")
        printer.text("--------------------------------\n")
        printer.set(align='center', width=2, height=2)
        printer.text(opc.mensaje)
        
        printer.text("\n\n\n\n\n\n")
        if tipo == 0:
            printer.cashdraw(2)
        printer.close()

    except Exception as e:
        pass
