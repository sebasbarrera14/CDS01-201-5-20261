from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.pedido import Pedido, ItemPedido
from models.carrito import Carrito
from models.cliente import Cliente

router = APIRouter()
TRANSICIONES = {'pendiente': ['pagado','cancelado'], 'pagado': ['en_preparacion','cancelado'], 'en_preparacion': ['enviado'], 'enviado': ['entregado'], 'entregado': [], 'cancelado': []}

class PedidoCreate(BaseModel):
    id_cliente: int
    direccion_entrega: str

class EstadoUpdate(BaseModel):
    nuevo_estado: str

@router.post('/', status_code=status.HTTP_201_CREATED)
def registrar_pedido(datos: PedidoCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == datos.id_cliente).first()
    if not cliente: raise HTTPException(status_code=404, detail='Cliente no encontrado')
    carrito = db.query(Carrito).filter(Carrito.id_cliente == datos.id_cliente).first()
    if not carrito or not carrito.items: raise HTTPException(status_code=400, detail='El carrito esta vacio')
    pedido = Pedido(id_cliente=datos.id_cliente, total=carrito.total, direccion_entrega=datos.direccion_entrega, estado='pendiente')
    db.add(pedido)
    db.flush()
    for item in carrito.items:
        db.add(ItemPedido(id_pedido=pedido.id_pedido, id_producto=item.id_producto, cantidad=item.cantidad, subtotal=item.subtotal))
        item.producto.stock -= item.cantidad
    for item in list(carrito.items): db.delete(item)
    carrito.total = 0.0
    db.commit()
    db.refresh(pedido)
    return {'mensaje': 'Pedido registrado', 'id_pedido': pedido.id_pedido, 'total': pedido.total, 'estado': pedido.estado}

@router.get('/cliente/{id_cliente}')
def historial_pedidos(id_cliente: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id_cliente == id_cliente).all()
    if not pedidos: raise HTTPException(status_code=404, detail='No se encontraron pedidos')
    return pedidos

@router.get('/{id_pedido}')
def obtener_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido: raise HTTPException(status_code=404, detail='Pedido no encontrado')
    return pedido

@router.patch('/{id_pedido}/estado')
def actualizar_estado(id_pedido: int, datos: EstadoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido: raise HTTPException(status_code=404, detail='Pedido no encontrado')
    if datos.nuevo_estado not in TRANSICIONES.get(pedido.estado, []): raise HTTPException(status_code=400, detail='Transicion no permitida')
    pedido.estado = datos.nuevo_estado
    db.commit()
    db.refresh(pedido)
    return {'mensaje': f'Estado actualizado a {datos.nuevo_estado}', 'id_pedido': pedido.id_pedido, 'estado': pedido.estado}

@router.delete('/{id_pedido}/cancelar')
def cancelar_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido: raise HTTPException(status_code=404, detail='Pedido no encontrado')
    if pedido.estado not in ['pendiente','pagado']: raise HTTPException(status_code=400, detail=f'No se puede cancelar en estado {pedido.estado}')
    for item in pedido.items: item.producto.stock += item.cantidad
    pedido.estado = 'cancelado'
    db.commit()
    return {'mensaje': 'Pedido cancelado y stock restaurado', 'id_pedido': pedido.id_pedido}
