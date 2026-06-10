from server import loadClubs


def test_load_clubs_returns_clubs_list():
    clubs = loadClubs()

    assert isinstance(clubs, list)
    assert len(clubs) > 0
    assert clubs[0]["name"] == "Simply Lift"
    assert clubs[0]["email"] == "john@simplylift.co"
    assert "points" in clubs[0]