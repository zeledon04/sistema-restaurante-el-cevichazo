from django.http import JsonResponse
from django.shortcuts import render

from restaurante.models import Platos, Productos
from ..view import datosUser
from ..utils import login_required
from django.templatetags.static import static


def  nuevaFacturaUnica(request):
    user_data = datosUser(request)
    datos = {**user_data}
    
    return render(request, 'pages/cuentas/agregarDelivery.html', datos)


@login_required
def buscar_productos(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        query = request.GET.get("q", "")
        
        print(f"Buscando productos con query: {query}")
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

        print(data)
        return JsonResponse({"productos": data})
    
    return JsonResponse({"error": "Peticion invalida"}, status=400)
