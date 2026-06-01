# Coquito Amarillo S.A.S. — Sistema de Gestión de Pedidos

> Práctica Final — Construcción de Software I
> Fundación Universitaria María Cano — 2026
> Fork de: luisfsanchezp/CDS01-201-5-20261

## Equipo
| Integrante | Rol |
|---|---|
| Johan Sebastián Barrera Rua | Backend Developer |
| Miguel Ángel González Estrada | Full Stack Developer |

## Descripción
WebApp con API-REST construida con FastAPI y SQLite que resuelve la problemática de gestión de pedidos de Coquito Amarillo S.A.S. Permite registrar clientes, gestionar productos, manejar carritos de compra, procesar pedidos y pagos con múltiples métodos.

## Problema que resuelve
Coquito Amarillo S.A.S. presentaba tiempos de carga superiores a 8 segundos, errores frecuentes en el carrito, ausencia de confirmaciones de pago y nula visibilidad del estado del pedido, lo que generó una caída del 35% en ventas en línea. Esta API resuelve cada uno de esos problemas.

## Stack Tecnológico
| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Framework | FastAPI |
| Base de datos | SQLite + SQLAlchemy |
| Seguridad | passlib + bcrypt |
| Pruebas | pytest + httpx |
| Entorno | GitHub Codespaces |
| Docs API | Swagger UI en /docs |

## Instalación y Ejecución

Clonar el repositorio:

git clone https://github.com/sebasbarrera14/CDS01-201-5-20261.git
cd CDS01-201-5-20261

Instalar dependencias:

pip install fastapi uvicorn sqlalchemy pydantic "passlib[bcrypt]" "bcrypt==4.0.1" httpx pytest pytest-cov python-multipart python-jose

Correr la aplicación:

uvicorn app:app --reload

Acceder a la documentación Swagger UI:

http://localhost:8000/docs

## Endpoints Principales

### Autenticación
| Método | Endpoint | Descripción |
|---|---|---|
| POST | /auth/registro | Registrar nuevo cliente |
| POST | /auth/login | Iniciar sesión |
| POST | /auth/logout/{id} | Cerrar sesión |

### Productos
| Método | Endpoint | Descripción |
|---|---|---|
| GET | /productos/ | Listar catálogo activo |
| GET | /productos/{id} | Detalle de producto |
| POST | /productos/ | Crear producto |
| PATCH | /productos/{id} | Actualizar producto |

### Carrito
| Método | Endpoint | Descripción |
|---|---|---|
| GET | /carrito/{id_cliente} | Ver carrito |
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

## Métodos de Pago Aceptados
- Tarjeta de crédito/débito
- PSE
- Efecty
- Nequi

## Estados del Pedido
pendiente → pagado → en_preparacion → enviado → entregado

pendiente → cancelado

pagado → cancelado

## Pruebas

pytest tests/ -v

## Estructura del Proyecto

app.py — Punto de entrada FastAPI
database.py — Configuración SQLAlchemy + SQLite
requirements.txt — Dependencias
models/ — Modelos de base de datos
  cliente.py
  producto.py
  carrito.py
  pedido.py
  pago.py
routers/ — Endpoints API-REST
  auth.py
  productos.py
  carrito.py
  pedidos.py
  pagos.py
tests/
  test_api.py — Pruebas automatizadas
docs/ — Documentación
  MANUAL_USUARIO.md
  MANUAL_TECNICO.md
  HISTORIAS_USUARIO.md
  DIAGRAMAS_UML.md
  diagrama_clases.svg
  diagrama_casos_uso.svg

## Ejemplo de Uso Rápido

import httpx

Registrar cliente:
httpx.post('http://localhost:8000/auth/registro', json={'nombre': 'Deisy Rodriguez', 'correo': 'deisy@gmail.com', 'contrasena': 'clave123'})

Crear producto:
httpx.post('http://localhost:8000/productos/', json={'nombre': 'Tenis Running', 'precio': 250000, 'stock': 100, 'categoria': 'Calzado'})
