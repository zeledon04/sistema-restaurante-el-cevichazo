CREATE TABLE usuarios (
    usuarioId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rol INTEGER NOT NULL -- 0: mesero, 1: admin, etc.
	user TEXT NOT NULL,
	contra TEXT NOT NULL,
);

-- Tabla: Mesas (sin UNIQUE en número)
CREATE TABLE mesas (
    mesaId INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL,
	mesero TEXT INTEGER NOT NULL
    estado INTEGER DEFAULT 0 -- 0: disponible, 1: ocupad
);

-- Tabla: Categorías para productos y platos
CREATE TABLE categoriasProducto (
    categoriaId INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
	estado INTEGER NOT NULL DEFAULT 1,
);

-- Tabla: Productos que se manejan por lotes (ej: cervezas)
CREATE TABLE productos (
    productoId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
	rutaFoto text,
    descripcion TEXT,
    precio REAL NOT NULL,
	stock integer not null,
	updated_at text, 
	estado INTEGER NOT NULL DEFAULT 1,
    categoriaId INTEGER NOT NULL,
    FOREIGN KEY (categoriaId) REFERENCES categoriasProducto(categoriaId)
);

-- Tabla: Lotes de productos
CREATE TABLE lotesProductos (
    loteId INTEGER PRIMARY KEY AUTOINCREMENT,
    productoId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
	precioCompraUnitario REAL,
    precioVenta real,
    fechaIngreso DATE NOT NULL DEFAULT CURRENT_DATE,
    fechaVencimiento DATE,
    estado INTEGER DEFAULT 1, -- 1: activo, 2: cerrado, 3: en espera
	stock integer not null,
    FOREIGN KEY (productoId) REFERENCES productos(productoId)
);

-- Tabla: Platos preparados (no por lote)
CREATE TABLE platos (
    platoId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
	rutaFoto TEXT,
    descripcion TEXT,
	updated_at TEXT, 
    precio REAL NOT NULL,
	estado INTEGER DEFAULT 1,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    categoriaId INTEGER,
    FOREIGN KEY (categoriaId) REFERENCES categoriasProducto(categoriaId)
);

-- Tabla: Cuentas temporales (pedidos abiertos por mesa)
CREATE TABLE cuentasTemporales (
    cuentaTemporalId INTEGER PRIMARY KEY AUTOINCREMENT,
    mesaId INTEGER NOT NULL,
    usuarioId INTEGER NOT NULL,
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER DEFAULT 0, -- 0: abierta, 1: cerrada
	clienteNombre TEXT DEFAULT "Generico", -- Cliente genérico sin tabla extra
    FOREIGN KEY (mesaId) REFERENCES mesas(mesaId),
    FOREIGN KEY (usuarioId) REFERENCES usuarios(usuarioId)
);

-- Detalles de cuenta temporal (productos por lote)
CREATE TABLE detalleCuentaTemporalProducto (
    detalleId INTEGER PRIMARY KEY AUTOINCREMENT,
    cuentaTemporalId INTEGER NOT NULL,
    productoId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (cuentaTemporalId) REFERENCES cuentasTemporales(cuentaTemporalId),
    FOREIGN KEY (productoId) REFERENCES productos(productoId)
);

-- Detalles de cuenta temporal (platos)
CREATE TABLE detalleCuentaTemporalPlato (
    detalleId INTEGER PRIMARY KEY AUTOINCREMENT,
    cuentaTemporalId INTEGER NOT NULL,
    platoId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (cuentaTemporalId) REFERENCES cuentasTemporales(cuentaTemporalId),
    FOREIGN KEY (platoId) REFERENCES platos(platoId)
);

-- Tabla: Facturas (registro final de una cuenta pagada)
CREATE TABLE facturas (
    facturaId INTEGER PRIMARY KEY AUTOINCREMENT,
    mesaId INTEGER NOT NULL,
    usuarioId INTEGER NOT NULL,
    clienteNombre TEXT, -- Cliente genérico sin tabla extra
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL,
    FOREIGN KEY (mesaId) REFERENCES mesas(mesaId),
    FOREIGN KEY (usuarioId) REFERENCES usuarios(usuarioId)
);

-- Detalles de factura (productos por lote)
CREATE TABLE detalleFacturaProducto (
    detalleId INTEGER PRIMARY KEY AUTOINCREMENT,
    facturaId INTEGER NOT NULL,
    productoId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precioUnitario REAL NOT NULL,
    FOREIGN KEY (facturaId) REFERENCES facturas(facturaId),
    FOREIGN KEY (productoId) REFERENCES productos(productoId)
);

-- Detalles de factura (platos)
CREATE TABLE detalleFacturaPlato (
    detalleId INTEGER PRIMARY KEY AUTOINCREMENT,
    facturaId INTEGER NOT NULL,
    platoId INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precioUnitario REAL NOT NULL,
    FOREIGN KEY (facturaId) REFERENCES facturas(facturaId),
    FOREIGN KEY (platoId) REFERENCES platos(platoId)
);

-- Historial de ventas (para resumen diario)
CREATE TABLE historialVentas (
    historialVentaId INTEGER PRIMARY KEY AUTOINCREMENT,
    productoId INTEGER,
    platoId INTEGER,
    cantidadTotal INTEGER NOT NULL,
    fechaVenta DATE NOT NULL,
    FOREIGN KEY (productoId) REFERENCES productos(productoId),
    FOREIGN KEY (platoId) REFERENCES platos(platoId)
);

-- Tabla cocinas
CREATE TABLE cocinas(
	cocinaId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	hora time NOT NULL,
	horaPreparacion time,
	horaFinalizada time,
	estado INTEGER NOT NULL DEFAULT 0, -- 0 = Pendiente, 1 = Listo, 2 = En proceso.
	mesaId INTEGER,
	platoId INTEGER NOT NULL,
	FOREIGN KEY (mesaId) REFERENCES mesas(mesaId),
	FOREIGN KEY (platoId) REFERENCES platos(platoId)
);

ALTER TABLE cocinas ADD COLUMN horaFinalizada time

--ALTER TABLE platos ADD COLUMN estado INTEGER DEFAULT 1
--ALTER TABLE platos ADD COLUMN rutaFoto TEXT
--ALTER TABLE platos ADD COLUMN updated_at TEXT
--ALTER TABLE cocinas RENAME COLUMN detalleId INTEGER TO detalleId INTEGER NULL;
--ALTER TABLE lotesProductos ADD COLUMN stock integer not null
--ALTER TABLE productos ADD COLUMN updated_at text
--ALTER TABLE categoriasProducto RENAME COLUMN descripcion to nombre

--INSERT INTO categoriasProducto (nombre, estado) VALUES (&quot;Cervezas&quot;, 1);


SELECT * FROM historialVentas    

INSERT INTO historialVentas (productoId, cantidadTotal, fechaVenta)
VALUES
(1, 3, DATE('now')), -- 3 cervezas hoy
(2, 2, DATE('now')); -- 2 refrescos hoy

INSERT INTO historialVentas (platoId, cantidadTotal, fechaVenta)
VALUES
(1, 1, DATE('now')), -- 1 pastel
(2, 3, DATE('now')); -- 3 tres leches

hra time DEFAULT CURRENT_TIME

SELECT productoId, SUM(cantidadTotal) AS total_vendido
FROM historialVentas
GROUP BY productoId

ALTER TABLE platos ADD COLUMN tiempo TEXT

SELECT * FROM cuentasTemporales

SELECT * FROM mesas

SELECT * FROM facturas

INSERT INTO cocinas (hora, mesaId, platoId)
VALUES ("09:38:10", 1, 3);

ALTER TABLE cocinas ADD COLUMN cliente TEXT