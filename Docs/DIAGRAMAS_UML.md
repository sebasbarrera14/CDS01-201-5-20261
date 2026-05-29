# Diagramas UML — Coquito Amarillo S.A.S.

---

## 1. Diagrama de Casos de Uso

### Actores
- **Cliente:** Usuario registrado que compra productos
- **Administrador:** Gestiona el catálogo y los pedidos
- **Operador Logístico:** Actualiza estados de envío vía API

### Casos de Uso por Actor

**Cliente:**
- CU-001 Registrarse e iniciar sesión
- CU-002 Explorar catálogo de productos
- CU-003 Gestionar carrito de compras
- CU-004 Registrar pedido
- CU-005 Procesar pago
- CU-006 Cancelar pedido
- CU-007 Consultar historial de pedidos

**Administrador:**
- CU-008 Gestionar inventario de productos
- CU-009 Gestionar pedidos del sistema

**Operador Logístico:**
- CU-010 Actualizar estado logístico del pedido

---

## 2. Diagrama de Clases

### Cliente
- id_cliente: int
- nombre: str
- correo: str
- contrasena_hash: str
- activo: bool
- intentos_fallidos: int
- fecha_registro: datetime
- autenticar(contrasena) -> bool
- cerrar_sesion() -> None
- desactivar_cuenta() -> None

### Producto
- id_producto: int
- nombre: str
- precio: float
- stock: int
- categoria: str
- activo: bool
- hay_disponibilidad(cantidad) -> bool
- reducir_stock(cantidad) -> None
- restaurar_stock(cantidad) -> None

### Carrito
- id_carrito: int
- id_cliente: int (FK -> Cliente)
- total: float
- fecha_actualizacion: datetime
- agregar_item(producto, cantidad) -> None
- modificar_cantidad(id_producto, nueva_cantidad) -> None
- eliminar_item(id_producto) -> None
- calcular_total() -> float
- vaciar() -> None

### ItemCarrito
- id_item: int
- id_carrito: int (FK -> Carrito)
- id_producto: int (FK -> Producto)
- cantidad: int
- subtotal: float

### Pedido
- id_pedido: int
- id_cliente: int (FK -> Cliente)
- total: float
- direccion_entrega: str
- estado: str
- fecha: datetime
- numero_seguimiento: str
- ESTADOS: ["pendiente","pagado","en_preparacion","enviado","entregado","cancelado"]
- TRANSICIONES: dict
- cambiar_estado(nuevo_estado) -> None
- cancelar() -> None
- generar_resumen() -> dict

### ItemPedido
- id_item: int
- id_pedido: int (FK -> Pedido)
- id_producto: int (FK -> Producto)
- cantidad: int
- subtotal: float

### Pago
- id_pago: int
- id_pedido: int (FK -> Pedido)
- metodo: str
- monto: float
- aprobado: bool
- fecha_pago: datetime
- referencia_transaccion: str
- METODOS: ["tarjeta","pse","efecty","nequi"]
- procesar() -> bool
- generar_comprobante() -> str

### Relaciones
- Cliente 1 ------ 1 Carrito (composición)
- Cliente 1 ------ * Pedido (asociación)
- Carrito 1 ------ * ItemCarrito (composición)
- Pedido 1 ------ * ItemPedido (composición)
- Pedido 1 ------ 1 Pago (composición)
- ItemCarrito * ------ 1 Producto (asociación)
- ItemPedido * ------ 1 Producto (asociación)

---

## 3. Diagrama de Arquitectura REST

+--------------------------------------------------+
|         Cliente HTTP / Swagger UI                |
|     Navegador · Postman · app móvil              |
+--------------------------------------------------+
                        |
                    HTTP Request
                        |
                        v
+--------------------------------------------------+
|              FastAPI — API Gateway               |
|    app.py · validación · serialización           |
|              documentación automática            |
+--------------------------------------------------+
                        |
                        v
+--------------------------------------------------+
|                    Routers                       |
|  auth.py | productos.py | carrito.py |           |
|  pedidos.py | pagos.py                           |
+--------------------------------------------------+
         |                          |
         v                          v
+--------------------+   +----------------------+
|  SQLAlchemy ORM    |   |   Notificaciones     |
|  database.py       |   |   services/          |
|  modelos · queries |   |   notificaciones.py  |
+--------------------+   +----------------------+
         |
         v
+--------------------------------------------------+
|                   SQLite                         |
|         coquito_amarillo.db · 7 tablas           |
|  clientes · productos · carritos · items_carrito |
|  pedidos · items_pedido · pagos                  |
+--------------------------------------------------+

---

## 4. Diagrama de Estados del Pedido

[pendiente] --> [pagado] --> [en_preparacion] --> [enviado] --> [entregado]
    |               |
    v               v
[cancelado]     [cancelado]

### Transiciones válidas:
| Estado Actual | Estados Siguientes Permitidos |
|---|---|
| pendiente | pagado, cancelado |
| pagado | en_preparacion, cancelado |
| en_preparacion | enviado |
| enviado | entregado |
| entregado | ninguno |
| cancelado | ninguno |
