import pytest
import httpx
from fastapi import status

@pytest.mark.asyncio
async def test_register_user(test_client, db):
    # Test successful registration
    response = test_client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "password": "newpass",
            "role": "customer"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    assert response.json()["role"] == "customer"

    # Test duplicate username
    response = test_client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "password": "newpass",
            "role": "customer"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_owner(test_client, test_users):
    # Test successful login for owner
    response = test_client.post(
        "/auth/login",
        data={"username": "owner", "password": "ownerpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test invalid password
    response = test_client.post(
        "/auth/login",
        data={"username": "owner", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_customer(test_client, test_users):
    # Test successful login for customer
    response = test_client.post(
        "/auth/login",
        data={"username": "customer", "password": "customerpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test invalid username
    response = test_client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "customerpass"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]