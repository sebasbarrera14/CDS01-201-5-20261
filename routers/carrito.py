from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.carrito import Carrito, ItemCarrito
from models.producto import Producto
from models.cliente import Cliente

router = APIRouter()

class AgregarItem(BaseModel):
    id_producto: int
    cantidad: int

@router.get('/{id_cliente}')
def obtener_carrito(id_cliente: int, db: Session = Depends(get_db)):
    carrito = db.query(Carrito).filter(Carrito.id_cliente == id_cliente).first()
    if not carrito:
        raise HTTPException(status_code=404, detail='Carrito no encontrado')
    return {
        'id_carrito': carrito.id_carrito,
        'id_cliente': carrito.id_cliente,
        'total': carrito.total,
        'items': [{'id_item': i.id_item, 'id_producto': i.id_producto, 'cantidad': i.cantidad, 'subtotal': i.subtotal} for i in carrito.items]
    }

@router.post('/{id_cliente}/items')
def agregar_item(id_cliente: int, datos: AgregarItem, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    producto = db.query(Producto).filter(Producto.id_producto == datos.id_producto).first()
    if not producto or not producto.activo:
        raise HTTPException(status_code=404, detail='Producto no disponible')
    if producto.stock < datos.cantidad:
        raise HTTPException(status_code=400, detail=f'Stock insuficiente. Disponible: {producto.stock}')
    carrito = db.query(Carrito).filter(Carrito.id_cliente == id_cliente).first()
    if not carrito:
        carrito = Carrito(id_cliente=id_cliente, total=0.0)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    item_existente = db.query(ItemCarrito).filter(ItemCarrito.id_carrito == carrito.id_carrito, ItemCarrito.id_producto == datos.id_producto).first()
    if item_existente:
        item_existente.cantidad += datos.cantidad
        item_existente.subtotal = item_existente.cantidad * producto.precio
    else:
        db.add(ItemCarrito(id_carrito=carrito.id_carrito, id_producto=datos.id_producto, cantidad=datos.cantidad, subtotal=datos.cantidad * producto.precio))
    db.flush()
    carrito.total = sum(i.subtotal for i in carrito.items)
    db.commit()
    db.refresh(carrito)
    return {'mensaje': 'Producto agregado al carrito', 'total': carrito.total}

@router.delete('/{id_cliente}/vaciar')
def vaciar_carrito(id_cliente: int, db: Session = Depends(get_db)):
    carrito = db.query(Carrito).filter(Carrito.id_cliente == id_cliente).first()
    if not carrito:
        raise HTTPException(status_code=404, detail='Carrito no encontrado')
    for item in carrito.items: db.delete(item)
    carrito.total = 0.0
    db.commit()
    return {'mensaje': 'Carrito vaciado exitosamente'}
