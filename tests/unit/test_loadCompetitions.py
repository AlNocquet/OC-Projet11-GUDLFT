from unittest.mock import mock_open, patch

from server import loadCompetitions


def test_load_competitions_returns_competitions_list():
    fake_json = """
    {
        "competitions": [
            {"name": "Spring Festival", "date": "2026-12-31 10:00:00", "numberOfPlaces": "25"}
        ]
    }
    """

    with patch("builtins.open", mock_open(read_data=fake_json)):
        competitions = loadCompetitions()

    assert isinstance(competitions, list)
    assert len(competitions) == 1
    assert competitions[0]["name"] == "Spring Festival"
    assert competitions[0]["date"] == "2026-12-31 10:00:00"
    assert competitions[0]["numberOfPlaces"] == "25"
