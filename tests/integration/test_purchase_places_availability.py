from server import app, clubs, competitions



def get_club(name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(name):
    return [competition for competition in competitions if competition["name"] == name][0]



# Happy path : 

def test_purchase_places_with_available_competition_places():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Fall Classic")

    club["points"] = "25"
    competition["numberOfPlaces"] = "13"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": "5",
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 20
    assert int(competition["numberOfPlaces"]) == 8



# Sad path :

def test_purchase_places_with_more_places_than_available():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Fall Classic")

    club["points"] = "25"
    competition["numberOfPlaces"] = "8"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": "10",
        },
    )

    assert response.status_code == 200
    assert b"There are not enough places available." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 8