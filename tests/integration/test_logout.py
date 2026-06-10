from server import app


def test_logout_redirects_to_index():
    client = app.test_client()

    response = client.get("/logout")

    assert response.status_code == 302
    assert response.location.endswith("/")