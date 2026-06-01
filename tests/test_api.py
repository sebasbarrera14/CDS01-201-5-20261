import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from app import app

TEST_DB_URL = 'sqlite:///./test_coquito.db'
engine_test = create_engine(TEST_DB_URL, connect_args={'check_same_thread': False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine_test)
client = TestClient(app)

def test_raiz():
    r = client.get('/')
    assert r.status_code == 200
    assert 'mensaje' in r.json()

def test_registrar_cliente():
    r = client.post('/auth/registro', json={'nombre': 'Test User', 'correo': 'test@test.com', 'contrasena': 'test123'})
    assert r.status_code == 201
    assert 'id_cliente' in r.json()

def test_login_exitoso():
    r = client.post('/auth/login', json={'correo': 'test@test.com', 'contrasena': 'test123'})
    assert r.status_code == 200
    assert r.json()['mensaje'] == 'Login exitoso'

def test_login_fallido():
    r = client.post('/auth/login', json={'correo': 'test@test.com', 'contrasena': 'incorrecta'})
    assert r.status_code == 401

def test_crear_producto():
    r = client.post('/productos/', json={'nombre': 'Coquito Test', 'precio': 3000.0, 'stock': 50, 'categoria': 'Bebidas'})
    assert r.status_code == 201
    assert 'id_producto' in r.json()

def test_listar_productos():
    r = client.get('/productos/')
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_producto_no_encontrado():
    r = client.get('/productos/9999')
    assert r.status_code == 404

def test_agregar_item_carrito():
    r = client.post('/carrito/1/items', json={'id_producto': 1, 'cantidad': 2})
    assert r.status_code == 200

def test_registrar_pedido():
    r = client.post('/pedidos/', json={'id_cliente': 1, 'direccion_entrega': 'Calle 123 Bogota'})
    assert r.status_code == 201
    assert r.json()['estado'] == 'pendiente'

def test_procesar_pago():
    r = client.post('/pagos/', json={'id_pedido': 1, 'metodo': 'nequi', 'monto': 7000.0})
    assert r.status_code == 200
    assert 'referencia' in r.json()
