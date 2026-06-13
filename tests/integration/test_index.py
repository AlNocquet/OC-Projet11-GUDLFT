from server import app


def test_index_displays_login_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Please enter your secretary email to continue:" in response.data
    assert b'name="email"' in response.data
    assert b"Enter" in response.data


def test_index_displays_login_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_index_displays_public_points_board():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Club Points Board" in response.data
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data