import pytest
import json
import uuid
from fastapi import status

@pytest.mark.asyncio
async def test_create_clinic_owner(test_client, test_users):
    # Login as owner
    login_response = test_client.post(
        "/auth/login",
        data={"username": "owner", "password": "ownerpass"}
    )
    token = login_response.json()["access_token"]

    # Test creating clinic (owner has access)
    clinic_data = {
        "name": "Test Clinic",
        "state": "Khartoum",
        "city": "Omdurman",
        "picture_url": "",
        "address": "123 Main Street",
        "phone_numbers": ["+249123456789"],
        "email": "test@clinic.com",
        "location_link": "https://maps.google.com/?q=15.5881,32.5666"
    }

    # Use multipart/form-data (clinic as JSON string)
    response = test_client.post(
        "/clinics/",
        data={"clinic": json.dumps(clinic_data)},
        files={},  # no picture uploaded
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Clinic"
    assert data["picture_url"] == ""
    return data.get("id")


@pytest.mark.asyncio
async def test_create_clinic_customer_denied(test_client, test_users):
    # Login as customer
    login_response = test_client.post(
        "/auth/login",
        data={"username": "customer", "password": "customerpass"}
    )
    token = login_response.json()["access_token"]

    clinic_data = {
        "name": "Customer Test Clinic",
        "state": "Khartoum",
        "city": "Omdurman",
        "address": "123 Main Street",
        "phone_numbers": ["+249123456789"],
        "email": "test@clinic.com",
        "location_link": "https://maps.google.com/?q=15.5881,32.5666"
    }

    response = test_client.post(
        "/clinics/",
        data={"clinic": json.dumps(clinic_data)},
        files={},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert "Insufficient permissions" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_clinics_customer(test_client, test_users, db):
    # Insert a test clinic
    clinic_id = str(uuid.uuid4())
    db.get_clinics_collection().insert_one({
        "id": clinic_id,
        "name": "Test Clinic",
        "state": "Khartoum",
        "city": "Omdurman",
        "address": "123 Main Street",
        "picture_url": "",
        "phone_numbers": ["+249123456789"],
        "email": "test@clinic.com",
        "location_link": "https://maps.google.com/?q=15.5881,32.5666"
    })

    # Login as customer
    login_response = test_client.post(
        "/auth/login",
        data={"username": "customer", "password": "customerpass"}
    )
    token = login_response.json()["access_token"]

    # Test getting clinics by state/city
    response = test_client.get(
        "/clinics?state=Khartoum&city=Omdurman",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Test Clinic"


@pytest.mark.asyncio
async def test_get_clinic_by_id_owner(test_client, test_users, db):
    clinic_id = str(uuid.uuid4())
    db.get_clinics_collection().insert_one({
        "id": clinic_id,
        "name": "Test Clinic",
        "state": "Khartoum",
        "city": "Omdurman",
        "address": "123 Main Street",
        "picture_url": "",
        "phone_numbers": ["+249123456789"],
        "email": "test@clinic.com",
        "location_link": "https://maps.google.com/?q=15.5881,32.5666"
    })

    # Login as owner
    login_response = test_client.post(
        "/auth/login",
        data={"username": "owner", "password": "ownerpass"}
    )
    token = login_response.json()["access_token"]

    response = test_client.get(
        f"/clinics/{clinic_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == clinic_id
    assert response.json()["picture_url"] == ""

    # Non-existent clinic
    response = test_client.get(
        f"/clinics/{str(uuid.uuid4())}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert "Clinic not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_unauthorized_access(test_client):
    response = test_client.get("/clinics?state=Khartoum&city=Omdurman")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

    response = test_client.post(
        "/clinics/",
        data={"clinic": json.dumps({
            "name": "Unauthorized Clinic",
            "state": "Khartoum",
            "city": "Omdurman",
            "address": "123 Main Street",
            "phone_numbers": ["+249123456789"],
            "email": "test@clinic.com",
            "location_link": "https://maps.google.com/?q=15.5881,32.5666"
        })},
        files={}
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]
