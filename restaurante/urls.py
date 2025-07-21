from django.contrib import admin
from django.urls import path
from . import view
from .views import cajas, mesas, platos, productos, categorias, lotes, opciones, cocinas
from .views.charts import ventas, productosVend

urlpatterns = [
    path('', view.login, name="login"),
    path("logout/", view.logout_view, name="logout"),

    path('dashboard/', view.dashboard, name='dashboard'),
    
    #urls para cajas
    path('verificar_caja/', cajas.verificar_caja, name='verificar_caja'),
    path('abrir_caja/', cajas.abrir_caja, name='abrir_caja'),
    # path('cerrar_caja/', cajas.cerrar_caja, name='cerrar_caja'),
    path('Cajas/listarCajas', cajas.listarCajas, name='listar_cajas'),
    # path('Cajas/detalleCaja/<int:cajaid>', cajas.detalleCaja, name='detalleCaja'),

    # urls para las mesas
    path('mesas/listar/', mesas.listarMesas, name='listar_mesas'),
    path('mesas/agregar/', mesas.agregarMesa, name='agregar_mesa'),
    path('mesas/agregarCuentas/<int:id>', mesas.agregarCuentas, name='agregar_cuentas'),
    path('api/meseros/', mesas.obtener_meseros, name='obtener_meseros'),
    
    
    path('buscar_productos/', facts.buscar_productos, name='buscar_productos'),
    path('cuentas/facturaUnica/', facts.nuevaFacturaUnica, name='nuevaFacturaUnica'),

    
    #urls para platos
    path('platos/listar/', platos.listarPlatos, name='listar_platos'),
    
    #urls para productos
    path('productos/listar', productos.listarProductos, name='listar_productos'),
    path('productos/listarInactivos', productos.listarProductosInactivos, name='listar_productos_inactivos'),
    path('productos/agregar/', productos.agregarProducto, name='agregar_producto'),
    path('productos/actualizarProducto/<int:id>', productos.actualizarProducto, name='actualizar_producto'),
    path('productos/eliminarProducto/<int:id>', productos.eliminarProducto, name='eliminar_producto'),
    path('productos/activarProducto/<int:id>', productos.activarProducto, name='activar_producto'),
    path('filtrar_productos/', productos.filtrar_productos, name='filtrar_productos'),
    
    #urls para lotes
    path('productos/listarLotes/<int:id>', lotes.listarLotes, name='listar_lotes'),
    path('productos/agregarLote/<int:id>', lotes.agregarLote, name='agregar_lote'),
    path('productos/cerrarLote/<int:id>', lotes.cerrarLote, name='cerrar_lote'),
    path('productos/eliminarLote/<int:id>', lotes.eliminarLote, name='eliminar_lote'),
    
    #urls para platos
    path('platos/listar', platos.listarPlatos, name='listar_platos'),
    path('platos/listarInactivos', platos.listarPlatosInactivos, name='listar_platos_inactivos'),
    path('platos/agregar', platos.agregarPlato, name='agregar_plato'),
    path('platos/actualizarPlato/<int:id>', platos.actualizarPlato, name='actualizar_plato'),
    path('platos/eliminarPlato/<int:id>', platos.eliminarPlato, name='eliminar_plato'),
    path('platos/activarPlato/<int:id>', platos.activarPlato, name='activar_plato'),
    
    #urls para categorias
    path('categorias/listar', categorias.listarCategorias, name='listar_categorias'),
    path('categorias/listarInactivas', categorias.listarCategoriasInactivas, name='listar_categorias_inactivas'),
    path('categorias/agregarCategoria', categorias.agregarCategoria, name='agregar_categoria'),
    path('categorias/actualizarCategoria/<int:id>', categorias.actualizarCategoria, name='actualizar_categoria'),
    path('categorias/eliminarCategoria/<int:id>', categorias.eliminarCategoria, name='eliminar_categoria'),
    path('categorias/activarCategoria/<int:id>', categorias.activarCategoria, name='activar_categoria'),
    
    #url para opciones
    path('opciones/', opciones.opciones, name='opciones'),
    
    #urls para ventas(Gráfico Dashboard)
    path('api/datos-grafico/', ventas.datos_grafico, name='datos_grafico'), 
    
    #urls para productos más vendidos(Gráfico Dashboard)
    path('api/productos_mas_vendidos/', productosVend.productos_mas_vendidos, name='productos_mas_vendidos'), 
    
    
    #urls para listar cocinas
    path('cocinas/listar/', cocinas.listarCocinas, name='listar_cocinas'),
    
]