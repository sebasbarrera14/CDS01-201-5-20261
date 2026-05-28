# Manual de Usuario — Coquito Amarillo S.A.S.

## ¿Qué es esta aplicación?
Sistema web para gestionar pedidos de Coquito Amarillo S.A.S. Permite registrarse, explorar el catálogo, agregar productos al carrito y realizar compras de forma segura.

---

## 1. Acceder a la aplicación
Una vez la app esté corriendo, abre tu navegador y entra a:
- Documentación interactiva: http://localhost:8000/docs
- Desde ahí puedes probar todos los endpoints sin necesidad de una interfaz adicional.

---

## 2. Registrarse
1. En Swagger UI busca la sección Autenticación
2. Haz clic en POST /auth/registro
3. Haz clic en Try it out
4. Ingresa tus datos — estos los inventas tú, son los que usarás para entrar al sistema:
   - nombre: tu nombre completo
   - correo: cualquier correo que quieras usar dentro del sistema
   - contrasena: la contraseña que quieras usar
5. Haz clic en Execute
6. Si el registro es exitoso recibirás tu id_cliente — guárdalo, lo necesitas para todo

---

## 3. Iniciar Sesión
1. Busca POST /auth/login
2. Ingresa el correo y contraseña que usaste al registrarte
3. Recibirás tu id_cliente y nombre
> Tras 5 intentos fallidos tu cuenta quedará bloqueada temporalmente

---

## 4. Explorar el Catálogo
1. Busca GET /productos/
2. Haz clic en Try it out → Execute
3. Verás la lista de productos disponibles con precio y stock
4. Puedes filtrar por categoría agregando el parámetro categoria

---

## 5. Agregar Productos al Carrito
1. Busca POST /carrito/{id_cliente}/items
2. Reemplaza {id_cliente} con tu id_cliente
3. Ingresa el id_producto y la cantidad deseada
4. El sistema validará el stock disponible automáticamente

---

## 6. Ver tu Carrito
1. Busca GET /carrito/{id_cliente}
2. Reemplaza {id_cliente} con tu id_cliente
3. Verás todos los productos agregados y el total

---

## 7. Registrar un Pedido
1. Busca POST /pedidos/
2. Ingresa tu id_cliente y dirección de entrega
3. El sistema creará el pedido en estado pendiente y vaciará el carrito automáticamente

---

## 8. Pagar el Pedido
1. Busca POST /pagos/
2. Ingresa el id_pedido que recibiste al registrar el pedido
3. Elige un método de pago — opciones disponibles: tarjeta, pse, efecty, nequi
4. El monto debe coincidir exactamente con el total del pedido
5. Si el pago es aprobado recibirás una referencia de transacción

---

## 9. Consultar el Estado del Pedido
1. Busca GET /pedidos/{id_pedido}
2. Reemplaza {id_pedido} con tu id_pedido

### Estados posibles:
| Estado | Descripción |
|---|---|
| pendiente | Pedido registrado, esperando pago |
| pagado | Pago confirmado |
| en_preparacion | Pedido siendo preparado |
| enviado | Pedido en camino |
| entregado | Pedido recibido |
| cancelado | Pedido cancelado |

---

## 10. Cancelar un Pedido
1. Busca DELETE /pedidos/{id_pedido}/cancelar
2. Solo se puede cancelar si el pedido está en estado pendiente o pagado
3. El stock de los productos se restaura automáticamente

---

## 11. Cerrar Sesión
1. Busca POST /auth/logout/{id_cliente}
2. Reemplaza {id_cliente} con tu id_cliente
3. Tu carrito se conserva para la próxima sesión
