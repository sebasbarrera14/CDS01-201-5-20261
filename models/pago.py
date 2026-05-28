from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Pago(Base):
    __tablename__ = 'pagos'
    id_pago                = Column(Integer, primary_key=True, index=True)
    id_pedido              = Column(Integer, ForeignKey('pedidos.id_pedido'))
    metodo                 = Column(String, nullable=False)
    monto                  = Column(Float, nullable=False)
    aprobado               = Column(Boolean, default=False)
    fecha_pago             = Column(DateTime, nullable=True)
    referencia_transaccion = Column(String, nullable=True)
    pedido                 = relationship('Pedido', back_populates='pago')
