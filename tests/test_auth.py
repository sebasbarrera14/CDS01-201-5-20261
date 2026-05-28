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


def test_registro_exitoso():
    """RF-001: Registro con datos válidos."""
    response = client.post("/auth/registro", json={
        "nombre": "María García",
        "correo": "maria@test.com",
        "contrasena": "clave123"
    })
    assert response.status_code == 201
    assert "id_cliente" in response.json()


def test_registro_correo_duplicado():
    """RF-001: No permite registrar el mismo correo dos veces."""
    client.post("/auth/registro", json={
        "nombre": "Juan López",
        "correo": "juan@test.com",
        "contrasena": "clave123"
    })
    response = client.post("/auth/registro", json={
        "nombre": "Juan López",
        "correo": "juan@test.com",
        "contrasena": "clave123"
    })
    assert response.status_code == 400


def test_login_exitoso():
    """RF-002: Login con credenciales correctas."""
    client.post("/auth/registro", json={
        "nombre": "Ana Torres",
        "correo": "ana@test.com",
        "contrasena": "clave123"
    })
    response = client.post("/auth/login", json={
        "correo": "ana@test.com",
        "contrasena": "clave123"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Ana Torres"


def test_login_contrasena_incorrecta():
    """RF-002: Login con contraseña incorrecta retorna 401."""
    client.post("/auth/registro", json={
        "nombre": "Pedro Ruiz",
        "correo": "pedro@test.com",
        "contrasena": "clave123"
    })
    response = client.post("/auth/login", json={
        "correo": "pedro@test.com",
        "contrasena": "incorrecta"
    })
    assert response.status_code == 401


def test_login_cliente_no_existe():
    """RF-002: Login con correo no registrado retorna 404."""
    response = client.post("/auth/login", json={
        "correo": "noexiste@test.com",
        "contrasena": "clave123"
    })
    assert response.status_code == 404


def test_bloqueo_tras_5_intentos():
    """RF-002: La cuenta se bloquea tras 5 intentos fallidos."""
    client.post("/auth/registro", json={
        "nombre": "Luis Mora",
        "correo": "luis@test.com",
        "contrasena": "clave123"
    })
    for _ in range(5):
        client.post("/auth/login", json={
            "correo": "luis@test.com",
            "contrasena": "incorrecta"
        })
    response = client.post("/auth/login", json={
        "correo": "luis@test.com",
        "contrasena": "clave123"
    })
    assert response.status_code == 403


def test_logout_exitoso():
    """RF-003: Cierre de sesión exitoso."""
    reg = client.post("/auth/registro", json={
        "nombre": "Sara Díaz",
        "correo": "sara@test.com",
        "contrasena": "clave123"
    })
    id_cliente = reg.json()["id_cliente"]
    response = client.post(f"/auth/logout/{id_cliente}")
    assert response.status_code == 200


def test_logout_cliente_no_existe():
    """RF-003: Logout con id inexistente retorna 404."""
    response = client.post("/auth/logout/99999")
    assert response.status_code == 404
