import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import json
import os
from app.main import app
from app.core.security import create_test_token

client = TestClient(app)

# Fixture per generare un token JWT valido per i test
@pytest.fixture
def valid_token():
    token_data = {
        "sub": "test_user",
        "iss": "PDND",
        "aud": "https://govway.publisys.it/govway/Regione/Eventi/v1",
        "iat": datetime.utcnow(),
        "nbf": datetime.utcnow(),
        "jti": "123456789",
        "client_id": "test_client",
        "purpose": "test"
    }
    return create_test_token(token_data, expires_delta=timedelta(minutes=30))

# Fixture per generare un token JWT scaduto per i test
@pytest.fixture
def expired_token():
    token_data = {
        "sub": "test_user",
        "iss": "PDND",
        "aud": "https://govway.publisys.it/govway/Regione/Eventi/v1",
        "iat": datetime.utcnow() - timedelta(hours=1),
        "nbf": datetime.utcnow() - timedelta(hours=1),
        "jti": "123456789",
        "client_id": "test_client",
        "purpose": "test",
        "exp": datetime.utcnow() - timedelta(minutes=5)  # Token scaduto 5 minuti fa
    }
    return create_test_token(token_data)

# Test per l'endpoint /status
def test_get_status(valid_token):
    response = client.get(
        "/status",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "online"

# Test per l'endpoint /status con formato XML
def test_get_status_xml(valid_token):
    response = client.get(
        "/status?format=xml",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "<status>" in response.text
    assert "</status>" in response.text

# Test per l'endpoint /eventi
def test_get_eventi(valid_token):
    response = client.get(
        "/eventi",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert "articles" in response.json()
    assert len(response.json()["articles"]) > 0
    assert "title" in response.json()["articles"][0]
    assert "description" in response.json()["articles"][0]
    assert "start_event_date" in response.json()["articles"][0]

# Test per l'endpoint /eventi con formato XML
def test_get_eventi_xml(valid_token):
    response = client.get(
        "/eventi?format=xml",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "<articles>" in response.text
    assert "<title>" in response.text

# Test per l'endpoint /eventi/date-search
def test_search_eventi_by_date(valid_token):
    response = client.get(
        "/eventi/date-search?start_date=2025-06-01&end_date=2025-07-31",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Verifica che gli eventi restituiti siano all'interno dell'intervallo di date specificato
    for evento in response.json():
        event_date = datetime.fromisoformat(evento["dataInizio"].split("T")[0])
        assert datetime(2025, 6, 1) <= event_date <= datetime(2025, 7, 31)

# Test per l'endpoint /eventi/date-search con date invalide
def test_search_eventi_by_date_invalid(valid_token):
    response = client.get(
        "/eventi/date-search?start_date=2025-07-31&end_date=2025-06-01",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["status"] == 400
    assert "La data di inizio deve essere precedente alla data di fine" in response.json()["detail"]

# Test per l'endpoint /auth-test
def test_auth_test(valid_token):
    response = client.get(
        "/auth-test",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Autenticazione riuscita"
    assert "payload" in response.json()

# Test per l'autenticazione con token mancante
def test_missing_token():
    response = client.get("/status")
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/problem+json"

# Test per l'autenticazione con token malformato
def test_malformed_token():
    response = client.get(
        "/status",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/problem+json"

# Test per l'autenticazione con token scaduto
def test_expired_token(expired_token):
    response = client.get(
        "/status",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/problem+json"
    assert "Token scaduto" in response.json()["detail"]
