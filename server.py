import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    matching_clubs = [ # ---------------------------------------------------------------> bug 1 (sécurisation du flux d’identification)
        club for club in clubs
        if club['email'] == request.form['email']
    ]

    if not matching_clubs:
        flash("Sorry, that email was not found.")
        return render_template('index.html')

    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    competition_date = datetime.strptime(
        foundCompetition['date'],
        "%Y-%m-%d %H:%M:%S"
    )

    if competition_date < datetime.now(): # -------------------------------------------> bug 5 (validation temporelle de la réservation)
        flash("You cannot book places for a past competition.")
        return render_template(
            'welcome.html',
            club=foundClub,
            competitions=competitions
        )

    return render_template(
        'booking.html',
        club=foundClub,
        competition=foundCompetition
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    matching_competitions = [
        competition for competition in competitions
        if competition['name'] == request.form['competition']
    ]

    competition = matching_competitions[0]

    matching_clubs = [
        club for club in clubs
        if club['name'] == request.form['club']
    ]

    club = matching_clubs[0]

    placesRequired = int(request.form['places'])


    if placesRequired > 12: # ----------------------------------------------------------> bug 4 (validation métier "no more than 12 places")
        flash('You cannot reserve more than 12 places.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )

    if placesRequired > int(club['points']): # ----------------------------------------> bug 2 (validation métier du solde de points)
        flash('You do not have enough points.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )

    if placesRequired > int(competition['numberOfPlaces']): # -------------------------> bug 3 (validation métier de la capacité restante)
        flash('There are not enough places available.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )

    competition['numberOfPlaces'] = (
        int(competition['numberOfPlaces']) - placesRequired
    )

    club['points'] = (
        int(club['points']) - placesRequired
    )

    flash('Great-booking complete!')

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions
    )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))