from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente        = Column(Integer, primary_key=True, index=True)
    nombre            = Column(String, nullable=False)
    correo            = Column(String, unique=True, nullable=False)
    contrasena_hash   = Column(String, nullable=False)
    activo            = Column(Boolean, default=True)
    intentos_fallidos = Column(Integer, default=0)
    fecha_registro    = Column(DateTime, default=datetime.now)
    pedidos           = relationship('Pedido', back_populates='cliente')
    carrito           = relationship('Carrito', back_populates='cliente', uselist=False)
