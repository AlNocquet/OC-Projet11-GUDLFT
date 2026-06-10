from server import app, clubs, competitions



def get_club(name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(name):
    return [competition for competition in competitions if competition["name"] == name][0]



# Happy path :

def test_purchase_places_with_enough_points():
    client = app.test_client()

    club = get_club("Simply Lift")
    competition = get_competition("Spring Festival")

    club["points"] = "13"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "5",
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 8
    assert int(competition["numberOfPlaces"]) == 20



# Sad path :

def test_purchase_places_with_not_enough_points():
    client = app.test_client()

    club = get_club("Iron Temple")
    competition = get_competition("Fall Classic")

    club["points"] = "4"
    competition["numberOfPlaces"] = "13"

    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Fall Classic",
            "places": "5",
        },
    )

    assert response.status_code == 200
    assert b"You do not have enough points." in response.data
    assert int(club["points"]) == 4
    assert int(competition["numberOfPlaces"]) == 13