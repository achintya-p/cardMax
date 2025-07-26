import pytest
from httpx import AsyncClient
from ..app.auth import get_password_hash

pytestmark = pytest.mark.asyncio

async def test_create_user(test_client, clean_db):
    response = await test_client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" in data

async def test_login(test_client, clean_db):
    # Create test user
    await test_client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    # Test login
    response = await test_client.post(
        "/token",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(test_client, clean_db):
    response = await test_client.post(
        "/token",
        data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

async def test_protected_endpoint(test_client, clean_db, test_user_token):
    # Test without token
    response = await test_client.get("/cards")
    assert response.status_code == 401
    
    # Test with token
    response = await test_client.get(
        "/cards",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200 