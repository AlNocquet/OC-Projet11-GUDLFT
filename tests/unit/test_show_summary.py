from server import app, clubs, competitions

# Happy path :
# email valide
# → accès welcome


def test_show_summary_with_valid_email():
    client = app.test_client()

    clubs[0]["points"] = "13"
    competitions[0]["numberOfPlaces"] = "25"

    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"}
    )

    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data
    assert b"Points available: 13" in response.data
    assert b"Spring Festival" in response.data


def test_show_summary_displays_club_points_board():
    client = app.test_client()

    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
    )

    assert response.status_code == 200
    assert b"Club Points Board" in response.data
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


    
# Sad path :
# email invalide
# → message erreur
# → pas crash


def test_show_summary_with_unknown_email():
    client = app.test_client()

    response = client.post(
        "/showSummary",
        data={"email": "unknown@email.com"}
    )

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Sorry, that email was not found." in response.data


def test_show_summary_with_empty_email():
    client = app.test_client()

    response = client.post(
        "/showSummary",
        data={"email": ""}
    )

    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Sorry, that email was not found." in response.data