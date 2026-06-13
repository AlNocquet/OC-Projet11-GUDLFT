import pytest
import server


@pytest.fixture
def fake_clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12",
        },
    ]


@pytest.fixture
def fake_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2026-12-31 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2026-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
        {
            "name": "Past Competition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "20",
        },
    ]


@pytest.fixture
def mocked_data(monkeypatch, fake_clubs, fake_competitions):
    monkeypatch.setattr(server, "clubs", fake_clubs)
    monkeypatch.setattr(server, "competitions", fake_competitions)
    return fake_clubs, fake_competitions


@pytest.fixture
def client(mocked_data):
    return server.app.test_client()