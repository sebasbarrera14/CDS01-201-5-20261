from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from database import get_db
from models.pago import Pago
from models.pedido import Pedido
router = APIRouter()
METODOS_VALIDOS = ['tarjeta', 'pse', 'efecty', 'nequi']
class PagoCreate(BaseModel):
    id_pedido: int
    metodo: str
    monto: float
@router.post('/')
def procesar_pago(datos: PagoCreate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == datos.id_pedido).first()
    if not pedido: raise HTTPException(status_code=404, detail='Pedido no encontrado')
    if pedido.estado != 'pendiente': raise HTTPException(status_code=400, detail='El pedido no esta en estado pendiente')
    if datos.metodo not in METODOS_VALIDOS: raise HTTPException(status_code=400, detail=f'Metodo no valido. Opciones: {METODOS_VALIDOS}')
    pago = Pago(id_pedido=datos.id_pedido, metodo=datos.metodo, monto=datos.monto, aprobado=True, fecha_pago=datetime.now(), referencia_transaccion=f'REF-{datos.id_pedido}-{int(datetime.now().timestamp())}')
    db.add(pago)
    pedido.estado = 'pagado'
    db.commit()
    db.refresh(pago)
    return {'mensaje': 'Pago aprobado', 'id_pago': pago.id_pago, 'referencia': pago.referencia_transaccion}
@router.get('/{id_pedido}')
def obtener_pago(id_pedido: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pedido == id_pedido).first()
    if not pago: raise HTTPException(status_code=404, detail='Pago no encontrado')
    return pago
