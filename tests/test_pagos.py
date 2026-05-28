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


def crear_pedido():
    """Helper: crea un cliente, producto, carrito y pedido listo para pagar."""
    ts = int(time.time() * 1000)
    cliente = client.post("/auth/registro", json={
        "nombre": "Test Pago",
        "correo": f"pago_{ts}@test.com",
        "contrasena": "clave123"
    })
    id_cliente = cliente.json()["id_cliente"]

    producto = client.post("/productos/", json={
        "nombre": f"Producto Test Pago {ts}",
        "precio": 60000,
        "stock": 10,
        "categoria": "test"
    })
    id_producto = producto.json()["id_producto"]

    client.post(f"/carrito/{id_cliente}/items", json={
        "id_producto": id_producto,
        "cantidad": 1
    })

    pedido = client.post("/pedidos/", json={
        "id_cliente": id_cliente,
        "direccion_entrega": "Calle 50 # 10-20, Bogotá"
    })
    return pedido.json()["id_pedido"], pedido.json()["total"]


def test_pago_exitoso():
    """RF-011: Procesa un pago válido correctamente."""
    id_pedido, total = crear_pedido()
    response = client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "pse",
        "monto": total
    })
    assert response.status_code == 200
    assert "referencia" in response.json()


def test_pago_metodo_invalido():
    """RF-011: Rechaza método de pago no válido."""
    id_pedido, total = crear_pedido()
    response = client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "bitcoin",
        "monto": total
    })
    assert response.status_code == 400


def test_pago_monto_incorrecto():
    """RF-011: Rechaza si el monto no coincide con el total del pedido."""
    id_pedido, total = crear_pedido()
    response = client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "tarjeta",
        "monto": total + 5000
    })
    assert response.status_code == 400


def test_pago_pedido_no_existe():
    """RF-011: Retorna 404 si el pedido no existe."""
    response = client.post("/pagos/", json={
        "id_pedido": 99999,
        "metodo": "nequi",
        "monto": 50000
    })
    assert response.status_code == 404


def test_pago_pedido_ya_pagado():
    """RF-011: No permite pagar un pedido que ya fue pagado."""
    id_pedido, total = crear_pedido()
    client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "efecty",
        "monto": total
    })
    response = client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "efecty",
        "monto": total
    })
    assert response.status_code == 400


def test_obtener_comprobante():
    """RF-013: Retorna el comprobante de pago de un pedido pagado."""
    id_pedido, total = crear_pedido()
    client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "nequi",
        "monto": total
    })
    response = client.get(f"/pagos/{id_pedido}")
    assert response.status_code == 200
    assert response.json()["aprobado"] == True


def test_comprobante_pedido_sin_pago():
    """RF-013: Retorna 404 si el pedido no tiene pago registrado."""
    id_pedido, _ = crear_pedido()
    response = client.get(f"/pagos/{id_pedido}")
    assert response.status_code == 404


def test_reembolso_exitoso():
    """RF-016: Inicia el reembolso de un pago aprobado."""
    id_pedido, total = crear_pedido()
    pago = client.post("/pagos/", json={
        "id_pedido": id_pedido,
        "metodo": "tarjeta",
        "monto": total
    })
    id_pago = pago.json()["id_pago"]
    response = client.post(f"/pagos/{id_pago}/reembolsar")
    assert response.status_code == 200
    assert "referencia_reembolso" in response.json()
