from flask import Flask, render_template, redirect, url_for, request, session

import sqlalchemy as db

import models
from dbConnection import DbConnection

app = Flask(__name__)
app.secret_key = 'super secret key'

dbConnection = DbConnection()


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        metadata = db.MetaData()
        s = db.select([models.kronikarz]).where(models.kronikarz.columns.email == request.form['email'])

        result = dbConnection.engine.execute(s)
        kronikarz = result.fetchone()
        if kronikarz is not None:
            if request.form['password'] != kronikarz.haslo:
                error = 'Spróbuj ponownie'
            else:
                session['id'] = kronikarz.nr_indeksu
                return redirect(url_for('profil'))
    return render_template('logowanie.html', error=error)


@app.route("/profil")
def profil():
    if session['id'] is not None:
        s = db.select([models.kronikarz]).where(models.kronikarz.columns.nr_indeksu == session['id'])

        result = dbConnection.engine.execute(s)
        kronikarz = result.fetchone()
        return render_template("profil.html", kronikarz=kronikarz)


@app.route("/zmien-dane")
def zmien_dane():
    if session['id'] is not None:
        return render_template("zmien_dane.html")


@app.route("/wnioski")
def wnioski():
    if session['id'] is not None:
        return render_template("wnioski.html")


@app.route("/zloz-wniosek")
def zloz_wniosek():
    if session['id'] is not None:
        return render_template("zloz_wniosek.html")


@app.route("/wydarzenia")
def wydarzenia():
    if session['id'] is not None:
        return render_template("wydarzenia.html")


@app.route("/utworz-wydarzenie")
def utworz_wydarzenie():
    if session['id'] is not None:
        return render_template("utworz_wydarzenie.html")


@app.route("/zadania-do-rozdzielenia")
def zadania_do_rozdzielenia():
    if session['id'] is not None:
        return render_template("zadania_do_rozdzielenia.html")


@app.route("/zadania-przydzielone")
def zadania_przydzielone():
    if session['id'] is not None:
        return render_template("zadania_przydzielone.html")


if __name__ == "__main__":
    dbConnection.engine.connect()
    app.run(debug=True)
