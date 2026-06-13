def get_club(clubs, name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(competitions, name):
    return [competition for competition in competitions if competition["name"] == name][0]


def test_purchase_places_deducts_club_points_after_successful_booking(client, mocked_data):
    clubs, competitions = mocked_data

    club = get_club(clubs, "Simply Lift")
    competition = get_competition(competitions, "Spring Festival")

    club["points"] = "13"
    competition["numberOfPlaces"] = "25"

    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 10
