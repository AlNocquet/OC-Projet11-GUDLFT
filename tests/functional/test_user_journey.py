from server import app, clubs, competitions


def test_user_can_login_book_places_and_see_confirmation():
    client = app.test_client()

    club = clubs[0]
    competition = competitions[2]

    club["points"] = "13"
    competition["numberOfPlaces"] = "20"

    login_response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
    )

    assert login_response.status_code == 200
    assert b"Welcome, john@simplylift.co" in login_response.data

    booking_page_response = client.get(
        f"/book/{competition['name']}/{club['name']}"
    )

    assert booking_page_response.status_code == 200
    assert b"How many places?" in booking_page_response.data

    purchase_response = client.post(
        "/purchasePlaces",
        data={
            "club": club["name"],
            "competition": competition["name"],
            "places": "3",
        },
    )

    assert purchase_response.status_code == 200
    assert b"Great-booking complete!" in purchase_response.data
    assert int(club["points"]) == 10
    assert int(competition["numberOfPlaces"]) == 17