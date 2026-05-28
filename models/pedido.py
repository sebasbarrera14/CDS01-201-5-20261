from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Pedido(Base):
    __tablename__ = 'pedidos'
    id_pedido          = Column(Integer, primary_key=True, index=True)
    id_cliente         = Column(Integer, ForeignKey('clientes.id_cliente'))
    total              = Column(Float, nullable=False)
    direccion_entrega  = Column(String, nullable=False)
    estado             = Column(String, default='pendiente')
    fecha              = Column(DateTime, default=datetime.now)
    numero_seguimiento = Column(String, nullable=True)
    cliente            = relationship('Cliente', back_populates='pedidos')
    items              = relationship('ItemPedido', back_populates='pedido')
    pago               = relationship('Pago', back_populates='pedido', uselist=False)

class ItemPedido(Base):
    __tablename__ = 'items_pedido'
    id_item     = Column(Integer, primary_key=True, index=True)
    id_pedido   = Column(Integer, ForeignKey('pedidos.id_pedido'))
    id_producto = Column(Integer, ForeignKey('productos.id_producto'))
    cantidad    = Column(Integer, nullable=False)
    subtotal    = Column(Float, nullable=False)
    pedido      = relationship('Pedido', back_populates='items')
    producto    = relationship('Producto')
