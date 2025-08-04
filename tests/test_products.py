import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from jose import jwt
from auth.jwt_handler import SECRET_KEY, ALGORITHM





@pytest.mark.asyncio
async def test_customer_login_returns_tokens():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", data={
            "username": "customer1",
            "password": "123",
            "grant_type": "password"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_vendor_login_returns_tokens_with_vendor_role():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", data={
            "username": "vendor1",
            "password": "123",
            "grant_type": "password"
        })
        assert response.status_code == 200
        token_payload = jwt.decode(response.json()["access_token"], SECRET_KEY, algorithms=["HS256"])
        assert token_payload["role"] == "vendor"


@pytest.mark.asyncio
async def test_admin_and_staff_login_return_correct_roles():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for user, role in [("admin1", "admin"), ("staff1", "staff")]:
            response = await client.post("/auth/login", data={
                "username": user,
                "password": "123",
                "grant_type": "password"
            })
            assert response.status_code == 200
            token = response.json()["access_token"]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            assert payload["role"] == role


@pytest.mark.asyncio
async def test_invalid_credentials_returns_401():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", data={
            "username": "nonexistent",
            "password": "wrong",
            "grant_type": "password"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_banned_user_cannot_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/auth/login", data={
            "username": "banned_user",
            "password": "123",
            "grant_type": "password"
        })
        assert response.status_code == 403
        assert response.json()["detail"] == "Inactive or banned user"
