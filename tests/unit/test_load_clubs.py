from unittest.mock import mock_open, patch

from server import loadClubs


def test_load_clubs_returns_clubs_list():
    fake_json = """
    {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
        ]
    }
    """

    with patch("builtins.open", mock_open(read_data=fake_json)):
        clubs = loadClubs()

    assert isinstance(clubs, list)
    assert len(clubs) == 1
    assert clubs[0]["name"] == "Simply Lift"
    assert clubs[0]["email"] == "john@simplylift.co"
    assert clubs[0]["points"] == "13"
