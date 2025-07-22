import json
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
                
            return JsonResponse({"success": True, "message": "Factura guardada correctamente"})
            
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})
        
    return JsonResponse({"success": False, "message": "Método no permitido"})
    
    
