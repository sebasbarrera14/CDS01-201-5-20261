import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from app import app

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine_test = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def crear_cliente_y_carrito():
    """Helper: crea un cliente, un producto y lo agrega al carrito."""
    ts = int(time.time() * 1000)
    cliente = client.post("/auth/registro", json={
        "nombre": "Test Pedido",
        "correo": f"pedido_{ts}@test.com",
        "contrasena": "clave123"
    })
    id_cliente = cliente.json()["id_cliente"]

    producto = client.post("/productos/", json={
        "nombre": f"Producto Test Pedido {ts}",
        "precio": 50000,
        "stock": 10,
        "categoria": "test"
    })
    id_producto = producto.json()["id_producto"]

    client.post(f"/carrito/{id_cliente}/items", json={
        "id_producto": id_producto,
        "cantidad": 2
    })
    return id_cliente, id_producto


def test_registrar_pedido_exitoso():
    """RF-014: Registra un pedido con carrito válido."""
    id_cliente, _ = crear_cliente_y_carrito()
    response = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    assert response.status_code == 201
    assert response.json()["estado"] == "pendiente"


def test_registrar_pedido_carrito_vacio():
    """RF-014: No permite registrar pedido con carrito vacío."""
    ts = int(time.time() * 1000)
    cliente = client.post("/auth/registro", json={
        "nombre": "Sin Carrito",
        "correo": f"sincarrito_{ts}@test.com",
        "contrasena": "clave123"
    })
    id_cliente = cliente.json()["id_cliente"]
    response = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    assert response.status_code == 400


def test_registrar_pedido_cliente_no_existe():
    """RF-014: Retorna 404 si el cliente no existe."""
    response = client.post("/pedidos/", json={
        "id_cliente": 99999,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    assert response.status_code == 404


def test_cambio_estado_valido():
    """RF-015: Permite transición válida de estado."""
    id_cliente, _ = crear_cliente_y_carrito()
    pedido = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    id_pedido = pedido.json()["id_pedido"]
    response = client.patch(f"/pedidos/{id_pedido}/estado", json={
        "nuevo_estado": "pagado"
    })
    assert response.status_code == 200
    assert response.json()["estado"] == "pagado"


def test_cambio_estado_invalido():
    """RF-015: Rechaza transición de estado no permitida."""
    id_cliente, _ = crear_cliente_y_carrito()
    pedido = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    id_pedido = pedido.json()["id_pedido"]
    response = client.patch(f"/pedidos/{id_pedido}/estado", json={
        "nuevo_estado": "entregado"
    })
    assert response.status_code == 400


def test_estado_no_reconocido():
    """RF-015: Rechaza estado no reconocido por el sistema."""
    id_cliente, _ = crear_cliente_y_carrito()
    pedido = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    id_pedido = pedido.json()["id_pedido"]
    response = client.patch(f"/pedidos/{id_pedido}/estado", json={
        "nuevo_estado": "inventado"
    })
    assert response.status_code == 400


def test_cancelar_pedido_pendiente():
    """RF-016: Cancela un pedido en estado pendiente."""
    id_cliente, _ = crear_cliente_y_carrito()
    pedido = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    id_pedido = pedido.json()["id_pedido"]
    response = client.delete(f"/pedidos/{id_pedido}/cancelar")
    assert response.status_code == 200


def test_cancelar_pedido_enviado():
    """RF-016: No permite cancelar un pedido en estado enviado."""
    id_cliente, _ = crear_cliente_y_carrito()
    pedido = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    id_pedido = pedido.json()["id_pedido"]
    client.patch(f"/pedidos/{id_pedido}/estado", json={"nuevo_estado": "pagado"})
    client.patch(f"/pedidos/{id_pedido}/estado", json={"nuevo_estado": "en_preparacion"})
    client.patch(f"/pedidos/{id_pedido}/estado", json={"nuevo_estado": "enviado"})
    response = client.delete(f"/pedidos/{id_pedido}/cancelar")
    assert response.status_code == 400


def test_historial_pedidos():
    """RF-017: Retorna el historial de pedidos del cliente."""
    id_cliente, _ = crear_cliente_y_carrito()
    client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 10 # 20-30, Medellín"
    })
    response = client.get(f"/pedidos/cliente/{id_cliente}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
