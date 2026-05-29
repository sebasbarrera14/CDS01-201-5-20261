# Manual Técnico — Coquito Amarillo S.A.S.

## Información General
- **Proyecto:** Sistema de Gestión de Pedidos
- **Institución:** Fundación Universitaria María Cano
- **Curso:** Construcción de Software I
- **Equipo:** Johan Sebastián Barrera Rua / Miguel Ángel González Estrada
- **Repositorio:** https://github.com/sebasbarrera14/CDS01-201-5-20261

---

## 1. Requisitos del Sistema
- Python 3.11 o superior
- pip
- Git
- Navegador web moderno

---

## 2. Instalación

Clonar el repositorio:
git clone https://github.com/sebasbarrera14/CDS01-201-5-20261.git
cd CDS01-201-5-20261

Instalar dependencias:
pip install -r requirements.txt

Correr la aplicación:
uvicorn app:app --reload

Acceder a la documentación en el navegador:
http://localhost:8000/docs

---

## 3. Estructura del Proyecto

app.py — Punto de entrada, registro de routers
database.py — Configuración de SQLAlchemy y SQLite
requirements.txt — Dependencias del proyecto
models/ — Modelos de la base de datos
  cliente.py — Tabla clientes
  producto.py — Tabla productos
  carrito.py — Tablas carritos e items_carrito
  pedido.py — Tablas pedidos e items_pedido
  pago.py — Tabla pagos
routers/ — Endpoints de la API REST
  auth.py — Registro, login, logout
  productos.py — CRUD de productos
  carrito.py — Gestión del carrito
  pedidos.py — Registro y estados de pedidos
  pagos.py — Procesamiento de pagos
services/
  notificaciones.py — Servicio de notificaciones

---

## 4. Base de Datos
El sistema usa SQLite con SQLAlchemy. La base de datos se crea automáticamente al correr la app por primera vez como archivo coquito_amarillo.db.

### Tablas principales:
| Tabla | Descripción |
|---|---|
| clientes | Usuarios registrados en el sistema |
| productos | Catálogo de productos disponibles |
| carritos | Carrito persistente por cliente |
| items_carrito | Productos dentro del carrito |
| pedidos | Órdenes de compra confirmadas |
| items_pedido | Productos dentro del pedido |
| pagos | Transacciones de pago |

---

## 5. API REST — Endpoints

### Autenticación
| Método | Endpoint | Descripción |
|---|---|---|
| POST | /auth/registro | Registrar nuevo cliente |
| POST | /auth/login | Iniciar sesión |
| POST | /auth/logout/{id_cliente} | Cerrar sesión |

### Productos
| Método | Endpoint | Descripción |
|---|---|---|
| GET | /productos/ | Listar productos activos |
| GET | /productos/{id} | Detalle de un producto |
| POST | /productos/ | Crear producto |
| PATCH | /productos/{id} | Actualizar producto |

### Carrito
| Método | Endpoint | Descripción |
|---|---|---|
| GET | /carrito/{id_cliente} | Ver carrito del cliente |
| POST | /carrito/{id_cliente}/items | Agregar ítem |
| PATCH | /carrito/{id_cliente}/items/{id_producto} | Modificar cantidad |
| DELETE | /carrito/{id_cliente}/items/{id_producto} | Eliminar ítem |
| DELETE | /carrito/{id_cliente}/vaciar | Vaciar carrito |

### Pedidos
| Método | Endpoint | Descripción |
|---|---|---|
| POST | /pedidos/ | Registrar pedido |
| GET | /pedidos/{id_pedido} | Detalle del pedido |
| GET | /pedidos/cliente/{id_cliente} | Historial de pedidos |
| PATCH | /pedidos/{id_pedido}/estado | Actualizar estado |
| DELETE | /pedidos/{id_pedido}/cancelar | Cancelar pedido |

### Pagos
| Método | Endpoint | Descripción |
|---|---|---|
| POST | /pagos/ | Procesar pago |
| GET | /pagos/{id_pedido} | Ver comprobante |

---

## 6. Normas de Calidad Aplicadas
- ISO/IEC 25010 — Funcionalidad, rendimiento, seguridad y mantenibilidad
- IEEE 730 — Plan de aseguramiento de calidad con revisiones y pruebas
- PEP-8 — Estándar de estilo de código Python
- TDD — Pruebas escritas antes de implementar cada función
