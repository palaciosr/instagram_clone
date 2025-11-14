import pytest

@pytest.mark.asyncio
async def test_user_flow(client):
    # Register
    r = await client.post("/api/users", json={
        "username": "alice",
        "password": "wonderland",
        "display_name": "Alice",
        "bio": "Hello World"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "alice"

    # Login
    r = await client.post("/api/users/token", data={
        "username": "alice",
        "password": "wonderland"
    })
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # Get /me
    r = await client.get("/api/users/me", headers=headers)
    assert r.status_code == 200
    me = r.json()
    assert me["username"] == "alice"
    assert me["display_name"] == "Alice"
