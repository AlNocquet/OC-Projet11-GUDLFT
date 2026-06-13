from server import app


def test_index_route_returns_200():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_ping_route_returns_pong():
    client = app.test_client()

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.data == b"pong"


def test_logout_redirects():
    client = app.test_client()

    response = client.get("/logout")

    assert response.status_code == 302