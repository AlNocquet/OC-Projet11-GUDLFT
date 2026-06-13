def get_club(clubs, name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(competitions, name):
    return [competition for competition in competitions if competition["name"] == name][0]


# Happy path:
# 12 places -> accepted


def test_purchase_places_with_12_places_limit(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "12"},
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 13
    assert int(competition["numberOfPlaces"]) == 13


# Sad path:
# 13 places -> rejected


def test_purchase_places_with_more_than_12_places(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "13"},
    )

    assert response.status_code == 200
    assert b"You must reserve between 1 and 12 places." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 25


# Sad path:
# 0 place -> rejected


def test_purchase_places_with_zero_place(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "0"},
    )

    assert response.status_code == 200
    assert b"You must reserve between 1 and 12 places." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 25


# Sad path:
# negative value -> rejected


def test_purchase_places_with_negative_place(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Spring Festival")

    club["points"] = "25"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "-1"},
    )

    assert response.status_code == 200
    assert b"You must reserve between 1 and 12 places." in response.data
    assert int(club["points"]) == 25
    assert int(competition["numberOfPlaces"]) == 25
