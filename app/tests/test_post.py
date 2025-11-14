import pytest

@pytest.mark.asyncio
async def test_post_flow(client):
    # Register and login user
    await client.post("/api/users", json={"username": "bob", "password": "secret"})
    r = await client.post("/api/users/token", data={"username": "bob", "password": "secret"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a post
    r = await client.post("/api/posts", json={
        "user_id": 1,
        "caption": "My first post"
    }, headers=headers)
    assert r.status_code == 201
    post = r.json()
    assert post["caption"] == "My first post"
    assert post["user_id"] == 1

    # Get feed
    r = await client.get("/api/posts/feed", headers=headers)
    assert r.status_code == 200
    feed = r.json()
    assert len(feed) == 1
    assert feed[0]["caption"] == "My first post"
