# Historias de Usuario — Coquito Amarillo S.A.S.

## Formato
Como [rol] quiero [acción] para [beneficio]

---

## Módulo de Autenticación

### HU-001 — Registro de cliente
Como visitante quiero registrarme con nombre, correo y contraseña para tener una cuenta y acceder al sistema.

Criterios de aceptación:
- El correo debe ser único en el sistema
- La contraseña se almacena cifrada con bcrypt
- Al registrarse exitosamente recibo mi id_cliente

---

### HU-002 — Inicio de sesión
Como cliente registrado quiero iniciar sesión con mi correo y contraseña para acceder a mi carrito y mis pedidos.

Criterios de aceptación:
- El sistema bloquea la cuenta tras 5 intentos fallidos
- Si las credenciales son correctas recibo confirmación con mi nombre
- Si el correo no existe recibo un mensaje de error claro

---

### HU-003 — Cierre de sesión
Como cliente registrado quiero cerrar sesión de forma segura para proteger mi cuenta en dispositivos compartidos.

Criterios de aceptación:
- El carrito se conserva al cerrar sesión
- El sistema confirma el cierre de sesión exitoso

---

## Módulo de Catálogo

### HU-004 — Ver catálogo de productos
Como cliente registrado quiero ver el catálogo completo de productos para explorar lo que está disponible y sus precios.

Criterios de aceptación:
- Solo se muestran productos activos
- Cada producto muestra nombre, precio, stock y categoría
- Puedo filtrar por categoría

---

### HU-005 — Ver detalle de un producto
Como cliente registrado quiero ver el detalle de un producto específico para decidir si lo quiero agregar al carrito.

Criterios de aceptación:
- Si el producto no existe recibo un mensaje de error
- Veo el stock disponible en tiempo real

---

## Módulo de Carrito

### HU-006 — Agregar producto al carrito
Como cliente registrado quiero agregar productos al carrito para acumular lo que quiero comprar antes de pagar.

Criterios de aceptación:
- El sistema valida que haya stock suficiente
- Si ya existe el producto en el carrito se suma la cantidad
- El total se recalcula automáticamente

---

### HU-007 — Modificar cantidad de un ítem
Como cliente registrado quiero modificar la cantidad de un producto en el carrito para ajustar mi compra antes de pagar.

Criterios de aceptación:
- El sistema valida que la nueva cantidad no supere el stock
- El total se recalcula automáticamente

---

### HU-008 — Eliminar producto del carrito
Como cliente registrado quiero eliminar un producto del carrito para descartar productos que ya no quiero comprar.

Criterios de aceptación:
- El producto se elimina y el total se recalcula
- El carrito puede quedar vacío sin errores

---

### HU-009 — Ver mi carrito
Como cliente registrado quiero ver el contenido de mi carrito para revisar lo que tengo antes de confirmar el pedido.

Criterios de aceptación:
- Veo todos los productos con cantidad y subtotal
- Veo el total general del carrito
- El carrito persiste entre sesiones

---

## Módulo de Pedidos

### HU-010 — Registrar pedido
Como cliente registrado quiero confirmar mi carrito como un pedido para iniciar el proceso de compra.

Criterios de aceptación:
- El carrito no puede estar vacío
- El sistema valida el stock antes de confirmar
- El pedido se crea en estado pendiente con un ID único
- El carrito se vacía automáticamente al confirmar

---

### HU-011 — Consultar estado del pedido
Como cliente registrado quiero consultar el estado actual de mi pedido para saber en qué etapa del proceso está mi compra.

Criterios de aceptación:
- Veo el estado actual y el detalle completo del pedido
- Los estados posibles son: pendiente, pagado, en_preparacion, enviado, entregado, cancelado

---

### HU-012 — Ver historial de pedidos
Como cliente registrado quiero ver el historial de todos mis pedidos para llevar un registro de mis compras anteriores.

Criterios de aceptación:
- Se listan todos los pedidos del cliente
- Si no hay pedidos recibo un mensaje informativo

---

### HU-013 — Cancelar pedido
Como cliente registrado quiero cancelar un pedido para desistir de una compra que ya no deseo.

Criterios de aceptación:
- Solo se puede cancelar si el pedido está en estado pendiente o pagado
- El stock de los productos se restaura automáticamente
- Si el pedido ya fue enviado no se puede cancelar

---

## Módulo de Pagos

### HU-014 — Pagar un pedido
Como cliente registrado quiero pagar mi pedido con el método de mi preferencia para completar mi compra.

Criterios de aceptación:
- Métodos aceptados: tarjeta, pse, efecty, nequi
- Si el pago es aprobado recibo una referencia de transacción
- Si el pago falla el pedido se cancela automáticamente

---

### HU-015 — Ver comprobante de pago
Como cliente registrado quiero ver el comprobante de mi pago para tener constancia de la transacción realizada.

Criterios de aceptación:
- Veo la referencia, método, monto y fecha del pago
- Solo disponible si el pago fue aprobado

---

## Módulo de Administración

### HU-016 — Crear producto
Como administrador quiero registrar nuevos productos en el catálogo para ampliar la oferta disponible para los clientes.

Criterios de aceptación:
- No se pueden crear productos duplicados con el mismo nombre y categoría
- El producto queda activo y visible en el catálogo inmediatamente

---

### HU-017 — Actualizar producto
Como administrador quiero actualizar el precio o stock de un producto para mantener el catálogo actualizado.

Criterios de aceptación:
- El stock no puede ser negativo
- Los cambios se reflejan en tiempo real en el catálogo

---

### HU-018 — Desactivar producto
Como administrador quiero desactivar un producto del catálogo para ocultarlo sin eliminarlo permanentemente.

Criterios de aceptación:
- El producto desactivado no aparece en el catálogo
- El producto puede reactivarse en cualquier momento
