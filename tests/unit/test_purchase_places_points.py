def get_club(clubs, name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(competitions, name):
    return [competition for competition in competitions if competition["name"] == name][0]


# Happy path:
# enough points -> booking accepted


def test_purchase_places_with_enough_points(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Spring Festival")

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "5"},
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 8
    assert int(competition["numberOfPlaces"]) == 20


# Sad path:
# not enough points -> booking rejected


def test_purchase_places_with_not_enough_points(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Iron Temple")
    competition = get_competition(competitions, "Fall Classic")

    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Fall Classic", "places": "5"},
    )

    assert response.status_code == 200
    assert b"You do not have enough points." in response.data
    assert int(club["points"]) == 4
    assert int(competition["numberOfPlaces"]) == 13
