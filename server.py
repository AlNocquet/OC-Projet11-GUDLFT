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
    return render_template(
        'index.html',
        clubs=clubs
    )


@app.route('/showSummary', methods=['POST'])
def showSummary():
    
    # bug 1 (sécurisation du flux d’identification)
    matching_clubs = [
        club for club in clubs
        if club['email'] == request.form['email']
    ]

    if not matching_clubs:
        flash("Sorry, that email was not found.")
        return render_template('index.html')

    # feature 7 (affichage du tableau des points des clubs) + template balises Nav
    club = matching_clubs[0]
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        clubs=clubs
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    competition_date = datetime.strptime(
        foundCompetition['date'],
        "%Y-%m-%d %H:%M:%S"
        )

    # bug 5 (validation temporelle de la réservation)
    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            'welcome.html',
            club=foundClub,
            competitions=competitions,
            clubs=clubs
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

    # bug 4 (validation métier "no more than 12 places")
    if placesRequired < 1 or placesRequired > 12:
        flash('You must reserve between 1 and 12 places.') # bug 4 (validation métier "no more than 12 places")
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )

    # bug 2 (validation du solde de points avant réservation)
    if placesRequired > int(club['points']):
        flash('You do not have enough points.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )

    # bug 3 (validation métier de la capacité restante)
    if placesRequired > int(competition['numberOfPlaces']):
        flash('There are not enough places available.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )


    # Mise à jour des places restantes dans la compétition
    competition['numberOfPlaces'] = (
        int(competition['numberOfPlaces']) - placesRequired
    )

    # bug 6 (déduction des points du club après réservation validée)
    club['points'] = ( 
        int(club['points']) - placesRequired
    )

    flash('Great-booking complete!')

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        clubs=clubs
    )


@app.route('/ping')
def ping():
    return "pong", 200

    
@app.route('/logout')
def logout():
    return redirect(url_for('index'))