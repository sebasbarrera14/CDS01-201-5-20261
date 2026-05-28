from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String, nullable=False)
    precio      = Column(Float, nullable=False)
    stock       = Column(Integer, default=0)
    categoria   = Column(String, nullable=False)
    activo      = Column(Boolean, default=True)
