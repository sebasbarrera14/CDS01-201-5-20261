# Coquito Amarillo S.A.S. — Sistema de Gestión de Pedidos

> Proyecto Final — Construcción de Software I
> Fundación Universitaria María Cano — 2026
> Forked from luisfsanchezp/CDS01-201-5-20261

## Equipo
| Integrante | Rol |
|---|---|
| Johan Sebastian Barrera Rua | Backend Developer |
| Miguel Angel Gonzalez Estrada | Full Stack Developer |

## Descripción
WebApp con API-REST construida con FastAPI y SQLite para gestionar clientes, productos y pedidos de Coquito Amarillo S.A.S.

## Stack Tecnológico
- Backend: FastAPI + Python 3.11
- Base de datos: SQLite + SQLAlchemy
- Pruebas: pytest + httpx
- CI/CD: GitHub Actions
- Entorno: GitHub Codespaces

## Instalación y Ejecución
1. Instalar dependencias: pip install -r requirements.txt
2. Correr la app: uvicorn app:app --reload
3. Abrir documentación: http://localhost:8000/docs

## Pruebas
Ejecutar: pytest tests/ -v --cov=.

## Endpoints Principales
| Módulo | Método | Endpoint | Descripción |
|---|---|---|---|
| Auth | POST | /auth/registro | Registrar cliente |
| Auth | POST | /auth/login | Iniciar sesión |
| Auth | POST | /auth/logout/{id} | Cerrar sesión |
| Productos | GET | /productos/ | Listar catálogo |
| Productos | POST | /productos/ | Crear producto |
| Carrito | GET | /carrito/{id} | Ver carrito |
| Carrito | POST | /carrito/{id}/items | Agregar ítem |
| Pedidos | POST | /pedidos/ | Registrar pedido |
| Pedidos | PATCH | /pedidos/{id}/estado | Actualizar estado |
| Pagos | POST | /pagos/ | Procesar pago |
