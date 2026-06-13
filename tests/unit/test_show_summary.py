# Happy path:
# valid email -> summary page


def test_show_summary_with_valid_email(client):
    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
    )

    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data
    assert b"Points available: 13" in response.data
    assert b"Spring Festival" in response.data


# Sad path:
# invalid email -> error message, no crash


def test_show_summary_with_unknown_email(client):
    response = client.post(
        "/showSummary",
        data={"email": "unknown@email.com"},
    )

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Sorry, that email was not found." in response.data


def test_show_summary_with_empty_email(client):
    response = client.post(
        "/showSummary",
        data={"email": ""},
    )

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Sorry, that email was not found." in response.data
