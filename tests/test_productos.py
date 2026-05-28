import pytest
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


def test_crear_producto_exitoso():
    """RF-023: Crea un producto con datos válidos."""
    response = client.post("/productos/", json={
        "nombre": "Canasta artesanal",
        "precio": 45000,
        "stock": 10,
        "categoria": "accesorios"
    })
    assert response.status_code == 201
    assert "id_producto" in response.json()


def test_crear_producto_duplicado():
    """RF-023: No permite crear un producto con el mismo nombre y categoría."""
    client.post("/productos/", json={
        "nombre": "Bolso wayuu",
        "precio": 85000,
        "stock": 5,
        "categoria": "bolsos"
    })
    response = client.post("/productos/", json={
        "nombre": "Bolso wayuu",
        "precio": 85000,
        "stock": 5,
        "categoria": "bolsos"
    })
    assert response.status_code == 400


def test_listar_productos():
    """RF-004: Lista todos los productos activos."""
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtrar_por_categoria():
    """RF-004: Filtra productos por categoría."""
    response = client.get("/productos/?categoria=accesorios")
    assert response.status_code == 200


def test_obtener_producto_existente():
    """RF-004: Retorna el detalle de un producto existente."""
    crear = client.post("/productos/", json={
        "nombre": "Mochila arhuaca",
        "precio": 120000,
        "stock": 3,
        "categoria": "mochilas"
    })
    id_producto = crear.json()["id_producto"]
    response = client.get(f"/productos/{id_producto}")
    assert response.status_code == 200


def test_obtener_producto_no_existente():
    """RF-004: Retorna 404 para producto inexistente."""
    response = client.get("/productos/99999")
    assert response.status_code == 404


def test_actualizar_stock():
    """RF-023: Actualiza el stock de un producto."""
    crear = client.post("/productos/", json={
        "nombre": "Sombrero vueltiao",
        "precio": 75000,
        "stock": 8,
        "categoria": "sombreros"
    })
    id_producto = crear.json()["id_producto"]
    response = client.patch(f"/productos/{id_producto}", json={"stock": 15})
    assert response.status_code == 200


def test_stock_negativo_rechazado():
    """RF-023: No permite stock negativo."""
    crear = client.post("/productos/", json={
        "nombre": "Collar de semillas",
        "precio": 25000,
        "stock": 5,
        "categoria": "joyeria"
    })
    id_producto = crear.json()["id_producto"]
    response = client.patch(f"/productos/{id_producto}", json={"stock": -1})
    assert response.status_code == 400


def test_desactivar_producto():
    """RF-023: Desactiva un producto."""
    crear = client.post("/productos/", json={
        "nombre": "Tapete tejido",
        "precio": 55000,
        "stock": 4,
        "categoria": "hogar"
    })
    id_producto = crear.json()["id_producto"]
    response = client.patch(f"/productos/{id_producto}", json={"activo": False})
    assert response.status_code == 200
