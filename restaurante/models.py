# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoriasproducto(models.Model):
    categoriaid = models.AutoField(db_column='categoriaId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    estado = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'categoriasProducto'


class Cuentastemporales(models.Model):
    cuentatemporalid = models.AutoField(db_column='cuentaTemporalId', primary_key=True, blank=True)  # Field name made lowercase.
    mesaid = models.ForeignKey('Mesas', models.DO_NOTHING, db_column='mesaId')  # Field name made lowercase.
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuarioId')  # Field name made lowercase.
    fechacreacion = models.DateTimeField(db_column='fechaCreacion', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    clientenombre = models.TextField(db_column='clienteNombre', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentasTemporales'


class Detallecuentatemporalplato(models.Model):
    detalleid = models.AutoField(db_column='detalleId', primary_key=True, blank=True)  # Field name made lowercase.
    cuentatemporalid = models.ForeignKey(Cuentastemporales, models.DO_NOTHING, db_column='cuentaTemporalId')  # Field name made lowercase.
    platoid = models.ForeignKey('Platos', models.DO_NOTHING, db_column='platoId')  # Field name made lowercase.
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detalleCuentaTemporalPlato'


class Detallecuentatemporalproducto(models.Model):
    detalleid = models.AutoField(db_column='detalleId', primary_key=True, blank=True)  # Field name made lowercase.
    cuentatemporalid = models.ForeignKey(Cuentastemporales, models.DO_NOTHING, db_column='cuentaTemporalId')  # Field name made lowercase.
    productoid = models.ForeignKey('Productos', models.DO_NOTHING, db_column='productoId')  # Field name made lowercase.
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detalleCuentaTemporalProducto'


class Detallefacturaplato(models.Model):
    detalleid = models.AutoField(db_column='detalleId', primary_key=True, blank=True)  # Field name made lowercase.
    facturaid = models.ForeignKey('Facturas', models.DO_NOTHING, db_column='facturaId')  # Field name made lowercase.
    platoid = models.ForeignKey('Platos', models.DO_NOTHING, db_column='platoId')  # Field name made lowercase.
    cantidad = models.IntegerField()
    preciounitario = models.FloatField(db_column='precioUnitario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalleFacturaPlato'


class Detallefacturaproducto(models.Model):
    detalleid = models.AutoField(db_column='detalleId', primary_key=True, blank=True)  # Field name made lowercase.
    facturaid = models.ForeignKey('Facturas', models.DO_NOTHING, db_column='facturaId')  # Field name made lowercase.
    productoid = models.ForeignKey('Productos', models.DO_NOTHING, db_column='productoId')  # Field name made lowercase.
    cantidad = models.IntegerField()
    preciounitario = models.FloatField(db_column='precioUnitario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalleFacturaProducto'


class Facturas(models.Model):
    facturaid = models.AutoField(db_column='facturaId', primary_key=True, blank=True)  # Field name made lowercase.
    mesaid = models.ForeignKey('Mesas', models.DO_NOTHING, db_column='mesaId')  # Field name made lowercase.
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuarioId')  # Field name made lowercase.
    clientenombre = models.TextField(db_column='clienteNombre', blank=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.FloatField()

    class Meta:
        managed = False
        db_table = 'facturas'


class Historialventas(models.Model):
    historialventaid = models.AutoField(db_column='historialVentaId', primary_key=True, blank=True)  # Field name made lowercase.
    productoid = models.ForeignKey('Productos', models.DO_NOTHING, db_column='productoId', blank=True)  # Field name made lowercase.
    platoid = models.ForeignKey('Platos', models.DO_NOTHING, db_column='platoId', blank=True)  # Field name made lowercase.
    cantidadtotal = models.IntegerField(db_column='cantidadTotal')  # Field name made lowercase.
    fechaventa = models.DateField(db_column='fechaVenta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'historialVentas'


class Lotesproductos(models.Model):
    loteid = models.AutoField(db_column='loteId', primary_key=True, blank=True)  # Field name made lowercase.
    productoid = models.ForeignKey('Productos', models.DO_NOTHING, db_column='productoId')  # Field name made lowercase.
    cantidad = models.IntegerField()
    fechaingreso = models.DateField(db_column='fechaIngreso')  # Field name made lowercase.
    fechavencimiento = models.DateField(db_column='fechaVencimiento', blank=True)  # Field name made lowercase.
    preciocompraunitario = models.FloatField(db_column='precioCompraUnitario', blank=True, null=True)  # Field name made lowercase.
    precioventa = models.FloatField(db_column='precioVenta', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(db_column='stock', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lotesProductos'


class Mesas(models.Model):
    mesaid = models.AutoField(db_column='mesaId', primary_key=True, blank=True)  # Field name made lowercase.
    numero = models.IntegerField()
    estado = models.IntegerField(blank=True, null=True)
    mesero = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mesas'


class Platos(models.Model):
    platoid = models.AutoField(db_column='platoId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.FloatField()
    rutafoto = models.TextField(db_column='rutaFoto', blank=True, null=True)  # Field name made lowercase.
    updated_at = models.DateTimeField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    categoriaid = models.ForeignKey(Categoriasproducto, models.DO_NOTHING, db_column='categoriaId', blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'platos'


class Productos(models.Model):
    productoid = models.AutoField(db_column='productoId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.FloatField()
    categoriaid = models.ForeignKey('Categoriasproducto', models.DO_NOTHING, db_column='categoriaId')  # Field name made lowercase.
    estado = models.IntegerField(blank=True, )
    rutafoto = models.TextField(db_column='rutaFoto', blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class Usuarios(models.Model):
    usuarioid = models.AutoField(db_column='usuarioId', primary_key=True, blank=True)  # Field name made lowercase.
    nombre = models.TextField()
    rol = models.IntegerField()
    user = models.TextField()
    contra = models.TextField()

    class Meta:
        managed = False
        db_table = 'usuarios'
        

class Cajas(models.Model):
    cajaid = models.AutoField(db_column='cajaId', primary_key=True, blank=True)  # Field name made lowercase.
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuarioId')  # Field name made lowercase.
    fechaapertura = models.DateTimeField(db_column='fechaApertura', blank=True, null=True)  # Field name made lowercase.
    fechaciere = models.DateTimeField(db_column='fechaCiere', blank=True, null=True)  # Field name made lowercase.
    cordobasinicial = models.FloatField(db_column='cordobasInicial')  # Field name made lowercase.
    dolaresinicial = models.FloatField(db_column='dolaresInicial')  # Field name made lowercase.
    cordobasfinal = models.FloatField(db_column='cordobasFinal', blank=True, null=True)  # Field name made lowercase.
    dolaresfinal = models.FloatField(db_column='dolaresFinal', blank=True, null=True)  # Field name made lowercase.
    totalingresos = models.FloatField(db_column='totalIngresos', blank=True, null=True)  # Field name made lowercase.
    sobrante = models.FloatField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    faltante = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cajas'
        

class Denominacionescaja(models.Model):
    denominacioncajaid = models.AutoField(db_column='denominacionCajaId', primary_key=True, blank=True)  
    cajaid = models.ForeignKey('Cajas', models.DO_NOTHING, db_column='cajaId')  
    tipodenominacion = models.IntegerField(db_column='tipoDenominacion')  
    denominacion = models.IntegerField()
    cantidad = models.IntegerField()
    tipomovimiento = models.IntegerField(db_column='tipoMovimiento')  
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'denominacionescaja'
        
        
class Opciones(models.Model):
    opcionid = models.AutoField(db_column='opcionId', primary_key=True, blank=True)  # Field name made lowercase.
    tasacambio = models.FloatField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opciones'
        