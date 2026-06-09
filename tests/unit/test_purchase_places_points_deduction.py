from server import app, clubs, competitions


def get_club(name):
    return [club for club in clubs if club["name"] == name][0]


def get_competition(name):
    return [competition for competition in competitions if competition["name"] == name][0]


def test_purchase_places_deducts_club_points_after_successful_booking():
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
            "places": "3",
        },
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(club["points"]) == 10