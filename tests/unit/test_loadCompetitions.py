from server import loadCompetitions


def test_load_competitions_returns_competitions_list():
    competitions = loadCompetitions()

    assert isinstance(competitions, list)
    assert len(competitions) > 0
    assert competitions[0]["name"] == "Spring Festival"
    assert competitions[0]["date"] == "2020-03-27 10:00:00"
    assert "numberOfPlaces" in competitions[0]