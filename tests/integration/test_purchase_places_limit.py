from server import app, clubs, competitions


def get_club(name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(name):
    return [competition for competition in competitions if competition["name"] == name][0]



# Happy path:
# 12 places -> accepted


def test_purchase_places_with_12_places_limit():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "12",
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 13
    assert int(competition["numberOfPlaces"]) == 13



# Sad path:
# 13 places -> rejected


def test_purchase_places_with_more_than_12_places():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "13",
        },
    )

    assert response.status_code == 200
    assert b"You must reserve between 1 and 12 places." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 25


def test_purchase_places_with_zero_place():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "0",
        },
    )

    assert response.status_code == 200
    assert b"You must reserve between 1 and 12 places." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 25


def test_purchase_places_with_negative_place():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "-1",
        },
    )

    assert response.status_code == 200
    assert b"You must reserve between 1 and 12 places." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 25