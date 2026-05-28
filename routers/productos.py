from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models.producto import Producto

router = APIRouter()

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: str

class ProductoUpdate(BaseModel):
    precio: Optional[float] = None
    stock: Optional[int] = None
    activo: Optional[bool] = None

@router.get('/')
def listar_productos(categoria: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Producto).filter(Producto.activo == True)
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    return query.all()

@router.get('/{id_producto}')
def obtener_producto(id_producto: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    if not producto:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return producto

@router.post('/', status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    existente = db.query(Producto).filter(Producto.nombre == datos.nombre, Producto.categoria == datos.categoria).first()
    if existente:
        raise HTTPException(status_code=400, detail='El producto ya existe en esa categoria')
    producto = Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return {'mensaje': 'Producto creado exitosamente', 'id_producto': producto.id_producto}

@router.patch('/{id_producto}')
def actualizar_producto(id_producto: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    if not producto:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    if datos.precio is not None: producto.precio = datos.precio
    if datos.stock is not None:
        if datos.stock < 0: raise HTTPException(status_code=400, detail='El stock no puede ser negativo')
        producto.stock = datos.stock
    if datos.activo is not None: producto.activo = datos.activo
    db.commit()
    db.refresh(producto)
    return {'mensaje': 'Producto actualizado', 'producto': {'id_producto': producto.id_producto, 'nombre': producto.nombre, 'precio': producto.precio, 'stock': producto.stock, 'activo': producto.activo}}
