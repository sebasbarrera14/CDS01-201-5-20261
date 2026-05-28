from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db
from models.cliente import Cliente

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class ClienteRegistro(BaseModel):
    nombre: str
    correo: str
    contrasena: str

class ClienteLogin(BaseModel):
    correo: str
    contrasena: str

@router.post('/registro', status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: ClienteRegistro, db: Session = Depends(get_db)):
    existente = db.query(Cliente).filter(Cliente.correo == datos.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail='El correo ya esta registrado')
    hash_pw = pwd_context.hash(datos.contrasena)
    cliente = Cliente(nombre=datos.nombre, correo=datos.correo, contrasena_hash=hash_pw)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return {'mensaje': 'Cliente registrado exitosamente', 'id_cliente': cliente.id_cliente}

@router.post('/login')
def iniciar_sesion(datos: ClienteLogin, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.correo == datos.correo).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    if not cliente.activo:
        raise HTTPException(status_code=403, detail='Cuenta bloqueada. Contacte soporte.')
    if not pwd_context.verify(datos.contrasena, cliente.contrasena_hash):
        cliente.intentos_fallidos += 1
        if cliente.intentos_fallidos >= 5:
            cliente.activo = False
        db.commit()
        raise HTTPException(status_code=401, detail='Credenciales incorrectas')
    cliente.intentos_fallidos = 0
    db.commit()
    return {'mensaje': 'Login exitoso', 'id_cliente': cliente.id_cliente, 'nombre': cliente.nombre}

@router.post('/logout/{id_cliente}')
def cerrar_sesion(id_cliente: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    return {'mensaje': f'Sesion cerrada para {cliente.nombre}'}
