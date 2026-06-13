def get_club(clubs, name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(competitions, name):
    return [competition for competition in competitions if competition["name"] == name][0]


# Happy path:
# enough competition places -> booking accepted


def test_purchase_places_with_available_competition_places(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Fall Classic")

    club["points"] = "25"
    competition["numberOfPlaces"] = "13"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Fall Classic", "places": "5"},
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 20
    assert int(competition["numberOfPlaces"]) == 8


# Sad path:
# more requested places than available -> booking rejected


def test_purchase_places_with_more_places_than_available(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Fall Classic")

    club["points"] = "25"
    competition["numberOfPlaces"] = "8"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Fall Classic", "places": "10"},
    )

    assert response.status_code == 200
    assert b"There are not enough places available." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 8
