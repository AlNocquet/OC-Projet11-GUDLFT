from datetime import datetime, timedelta


def get_competition(competitions, name):
    return [competition for competition in competitions if competition["name"] == name][0]


# Happy path:
# future competition -> booking page displayed


def test_book_future_competition(client, mocked_data):
    clubs, competitions = mocked_data
    competition = get_competition(competitions, "Spring Festival")

    competition["date"] = (
        datetime.now() + timedelta(days=30)
    ).strftime("%Y-%m-%d %H:%M:%S")

    response = client.get("/book/Spring%20Festival/Simply%20Lift")

    assert response.status_code == 200
    assert b"Booking for Spring Festival" in response.data
    assert b"How many places?" in response.data


# Sad path:
# past competition -> booking page blocked


def test_book_past_competition(client, mocked_data):
    clubs, competitions = mocked_data
    competition = get_competition(competitions, "Spring Festival")

    competition["date"] = (
        datetime.now() - timedelta(days=30)
    ).strftime("%Y-%m-%d %H:%M:%S")

    response = client.get("/book/Spring%20Festival/Simply%20Lift")

    assert response.status_code == 200
    assert b"You cannot book places for a past competition." in response.data
    assert b"How many places?" not in response.data
