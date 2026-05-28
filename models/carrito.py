from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Carrito(Base):
    __tablename__ = 'carritos'
    id_carrito          = Column(Integer, primary_key=True, index=True)
    id_cliente          = Column(Integer, ForeignKey('clientes.id_cliente'))
    total               = Column(Float, default=0.0)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    cliente             = relationship('Cliente', back_populates='carrito')
    items               = relationship('ItemCarrito', back_populates='carrito')

class ItemCarrito(Base):
    __tablename__ = 'items_carrito'
    id_item     = Column(Integer, primary_key=True, index=True)
    id_carrito  = Column(Integer, ForeignKey('carritos.id_carrito'))
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
    cantidad    = Column(Integer, nullable=False)
    subtotal    = Column(Float, nullable=False)
    carrito     = relationship('Carrito', back_populates='items')
    producto    = relationship('Producto')
