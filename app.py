from fastapi import FastAPI
from database import engine, Base
from routers import auth, productos, carrito, pedidos, pagos
import models.cliente, models.producto, models.carrito, models.pedido, models.pago

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Coquito Amarillo S.A.S. — API REST',
    description='Sistema de gestion de pedidos para Coquito Amarillo S.A.S.',
    version='1.0.0'
)

app.include_router(auth.router,      prefix='/auth',      tags=['Autenticacion'])
app.include_router(productos.router, prefix='/productos',  tags=['Productos'])
app.include_router(carrito.router,   prefix='/carrito',   tags=['Carrito'])
app.include_router(pedidos.router,   prefix='/pedidos',   tags=['Pedidos'])
app.include_router(pagos.router,     prefix='/pagos',     tags=['Pagos'])

@app.get('/', tags=['Root'])
def root():
    return {'mensaje': 'Bienvenido a la API de Coquito Amarillo S.A.S.', 'docs': '/docs', 'version': '1.0.0'}
