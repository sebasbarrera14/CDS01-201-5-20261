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
 
# ── Pruebas originales ────────────────────────────────────────────────────────
 
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
 
# ── Pruebas adicionales — Productos ──────────────────────────────────────────
 
def test_obtener_producto_por_id():
    r = client.get('/productos/1')
    assert r.status_code == 200
    assert 'nombre' in r.json()
 
def test_actualizar_producto():
    r = client.patch('/productos/1', json={'precio': 3500.0, 'stock': 40})
    assert r.status_code == 200
    assert r.json()['producto']['precio'] == 3500.0
 
def test_actualizar_producto_stock_negativo():
    r = client.patch('/productos/1', json={'stock': -5})
    assert r.status_code == 400
 
def test_crear_producto_duplicado():
    r = client.post('/productos/', json={'nombre': 'Coquito Test', 'precio': 3000.0, 'stock': 50, 'categoria': 'Bebidas'})
    assert r.status_code == 400
 
def test_listar_productos_por_categoria():
    r = client.get('/productos/?categoria=Bebidas')
    assert r.status_code == 200
    assert isinstance(r.json(), list)
 
# ── Pruebas adicionales — Carrito ─────────────────────────────────────────────
 
def test_ver_carrito():
    client.post('/auth/registro', json={'nombre': 'User Carrito', 'correo': 'carrito@test.com', 'contrasena': 'test123'})
    client.post('/carrito/2/items', json={'id_producto': 1, 'cantidad': 1})
    r = client.get('/carrito/2')
    assert r.status_code == 200
    assert 'items' in r.json()
 
def test_carrito_no_encontrado():
    r = client.get('/carrito/9999')
    assert r.status_code == 404
 
def test_agregar_item_stock_insuficiente():
    r = client.post('/carrito/1/items', json={'id_producto': 1, 'cantidad': 99999})
    assert r.status_code == 400
 
def test_vaciar_carrito():
    client.post('/carrito/2/items', json={'id_producto': 1, 'cantidad': 1})
    r = client.delete('/carrito/2/vaciar')
    assert r.status_code == 200
    assert 'vaciado' in r.json()['mensaje'].lower()
 
# ── Pruebas adicionales — Pedidos ─────────────────────────────────────────────
 
def test_obtener_pedido_por_id():
    r = client.get('/pedidos/1')
    assert r.status_code == 200
    assert 'estado' in r.json()
 
def test_pedido_no_encontrado():
    r = client.get('/pedidos/9999')
    assert r.status_code == 404
 
def test_historial_pedidos_cliente():
    r = client.get('/pedidos/cliente/1')
    assert r.status_code == 200
    assert isinstance(r.json(), list)
 
def test_historial_pedidos_cliente_sin_pedidos():
    client.post('/auth/registro', json={'nombre': 'Sin Pedidos', 'correo': 'sinpedidos@test.com', 'contrasena': 'test123'})
    r = client.get('/pedidos/cliente/3')
    assert r.status_code == 404
 
def test_actualizar_estado_pedido():
    client.post('/auth/registro', json={'nombre': 'User Estado', 'correo': 'estado@test.com', 'contrasena': 'test123'})
    client.post('/carrito/4/items', json={'id_producto': 1, 'cantidad': 1})
    r_pedido = client.post('/pedidos/', json={'id_cliente': 4, 'direccion_entrega': 'Calle 456'})
    id_pedido = r_pedido.json()['id_pedido']
    client.post('/pagos/', json={'id_pedido': id_pedido, 'metodo': 'pse', 'monto': 3500.0})
    r = client.patch(f'/pedidos/{id_pedido}/estado', json={'nuevo_estado': 'en_preparacion'})
    assert r.status_code == 200
    assert r.json()['estado'] == 'en_preparacion'
 
def test_cancelar_pedido():
    client.post('/auth/registro', json={'nombre': 'User Cancel', 'correo': 'cancel@test.com', 'contrasena': 'test123'})
    client.post('/carrito/5/items', json={'id_producto': 1, 'cantidad': 1})
    r_pedido = client.post('/pedidos/', json={'id_cliente': 5, 'direccion_entrega': 'Calle 789'})
    id_pedido = r_pedido.json()['id_pedido']
    r = client.delete(f'/pedidos/{id_pedido}/cancelar')
    assert r.status_code == 200
    assert 'cancelado' in r.json()['mensaje'].lower()
 
# ── Pruebas adicionales — Pagos ───────────────────────────────────────────────
 
def test_obtener_comprobante_pago():
    r = client.get('/pagos/1')
    assert r.status_code == 200
    assert 'referencia_transaccion' in r.json()
 
def test_pago_metodo_invalido():
    client.post('/auth/registro', json={'nombre': 'User Pago', 'correo': 'pago@test.com', 'contrasena': 'test123'})
    client.post('/carrito/6/items', json={'id_producto': 1, 'cantidad': 1})
    r_pedido = client.post('/pedidos/', json={'id_cliente': 6, 'direccion_entrega': 'Calle 000'})
    id_pedido = r_pedido.json()['id_pedido']
    r = client.post('/pagos/', json={'id_pedido': id_pedido, 'metodo': 'bitcoin', 'monto': 3500.0})
    assert r.status_code == 400
 
# ── Pruebas adicionales — Auth ────────────────────────────────────────────────
 
def test_registro_correo_duplicado():
    r = client.post('/auth/registro', json={'nombre': 'Duplicado', 'correo': 'test@test.com', 'contrasena': 'test123'})
    assert r.status_code == 400
 
def test_logout():
    r = client.post('/auth/logout/1')
    assert r.status_code == 200
    assert 'mensaje' in r.json()
