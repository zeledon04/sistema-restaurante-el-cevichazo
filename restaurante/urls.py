from django.contrib import admin
from django.urls import path
from . import view
from .views import cajas, facts, mesas, platos, usuarios, ventasPDF, ventasDelDia,productos, categorias, lotes, opciones, facturas, cocinas, cuentas, respaldos
from .views.charts import ventas, productosVend

urlpatterns = [
    path('', view.login, name="login"),
    path("logout/", view.logout_view, name="logout"),

    path('dashboard/', view.dashboard, name='dashboard'),
    
        #urls de historial de facturas
    path('Factura/historial', facturas.historialFacturacion, name='historial_facturas'),
    path('factura/detalle/<int:factura_id>/', facturas.detalle_factura_json, name='detalle_factura_json'),
    path('filtrar_facturas/', facturas.filtrar_facturas, name='filtrar_facturas'),
    path('Facturas/anularFactura/<int:facturaid>', facturas.anularFactura, name='anularFactura'),
    
    #url de registro de ventas pdf
    path('registroVentas/pdf/', ventasPDF.registro_ventas_pdf, name='registro_ventas_pdf'),
    path('registroVentas/imprimir/', ventasPDF.imprimir_registro_ventas, name='imprimir_registro_ventas'),
    
    path('registroVentasDelDia/pdf/', ventasDelDia.registro_ventas_del_dia_pdf, name='registro_ventas_del_dia_pdf'),
    path('registroVentasDelDia/imprimir/', ventasDelDia.imprimir_registro_ventas_del_dia, name='imprimir_registro_ventas_del_dia'),
    
    #url de registro de facturas pdf
    path('registroFacturas/pdf/', facturas.registro_factura_pdf, name='registro_factura_pdf'),
    path('registroFacturas/imprimir/', facturas.imprimir_registro_facturas, name='imprimir_registro_facturas'),
    
    
    #urls para cajas
    path('verificar_caja/', cajas.verificar_caja, name='verificar_caja'),
    path('abrir_caja/', cajas.abrir_caja, name='abrir_caja'),
    path('cerrar_caja/', cajas.cerrar_caja, name='cerrar_caja'),
    path('Cajas/listarCajas', cajas.listarCajas, name='listar_cajas'),
    path('Cajas/detalleCaja/<int:cajaid>', cajas.detalleCaja, name='detalleCaja'),

    # urls para las mesas
    path('mesas/listar/', mesas.listarMesas, name='listar_mesas'),
    path('mesas/agregar/', mesas.agregarMesa, name='agregar_mesa'),
    path('api/meseros/', mesas.obtener_meseros, name='obtener_meseros'),
    
    #urls para cuentas
    path('cuentas/agregarCuentas/<int:id>', cuentas.agregarCuentas, name='agregar_cuentas'),
    path('cuentas/crearCuenta/', cuentas.crear_cuenta_temporal, name='crear_cuenta_temporal'),
    path('actualizar_cuenta_temporal/', cuentas.actualizar_cuenta_temporal, name='actualizar_cuenta_temporal'),
    path('eliminar_detalle_cuenta/', cuentas.eliminar_detalle_cuenta, name='eliminar_detalle_cuenta'),
    path('eliminar_cuenta_temporal/', cuentas.eliminar_cuenta_temporal, name='eliminar_cuenta_temporal'),
    path('imprimir-precuenta/', cuentas.imprimir_precuenta, name='imprimir_precuenta'),


    path('buscar_productos/', facts.buscar_productos, name='buscar_productos'),
    path('cuentas/facturaUnica/', facts.nueva_Factura_Unica, name='nuevaFacturaUnica'),
    path('guardar-factura-unica/', facts.guardar_Factura_Unica, name='guardarFacturaUnica'),

    
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
    path('Productos/historialVentas', productos.historialVentas, name='historial_ventas'),
    path('filtrar-ventas/', productos.filtrar_ventas, name='filtrar_ventas'),
    
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
    path('cocina/estado/', cocinas.cocina_estado, name='cocina_estado'),
    path('enviar-a-cocina/', cocinas.enviar_a_cocina, name='enviar_a_cocina'),
    path('cambiar-estado-cocina/<int:cocina_id>/', cocinas.cambiar_estado_cocina, name='cambiar_estado_cocina'),
    
    path('api/tasa-cambio/', view.obtener_tasa_cambio, name='tasa_cambio'),
    
    #urls para usuarios
    path('usuarios/listar', usuarios.listarUsuarios, name='listar_usuarios'),
    path('usuarios/listarInactivos', usuarios.listarUsuariosInactivos, name='listar_usuarios_inactivos'),
    path('usuarios/agregarUsuario', usuarios.agregarUsuario, name='agregar_usuario'),
    path('usuarios/actualizarUsuario/<int:id>', usuarios.actualizarUsuario, name='actualizar_usuario'),
    path('usuarios/eliminarUsuario/<int:id>', usuarios.eliminarUsuario, name='eliminar_usuario'),
    path('usuarios/activarUsuario/<int:id>', usuarios.activarUsuario, name='activar_usuario'),
    
    path('respaldar-db/', respaldos.respaldar_db, name='respaldar_db'),
    path('imprimir-factura/<int:facturaid>/', facts.imprimir_factura, name='imprimir_factura'),
]