from flask import Flask, render_template, redirect, url_for, request

import sqlalchemy as db

from engine import Engine

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #metadata = db.MetaData()
        #kronikarz = db.Table('kronikarz', metadata, autoload=True, autoload_with=engine)
        #password = db.select([kronikarz]).where(kronikarz.columns.email == request.form['email'])
        if request.form['password'] != "admin":
            error = 'Spróbuj ponownie'
        else:
            return redirect(url_for('profil'))
    return render_template('logowanie.html', error=error)


@app.route("/profil")
def profil():
    return render_template("profil.html")


@app.route("/zmien-dane")
def zmien_dane():
    return render_template("zmien_dane.html")


@app.route("/wnioski")
def wnioski():
    return render_template("wnioski.html")


@app.route("/zloz-wniosek")
def zloz_wniosek():
    return render_template("zloz_wniosek.html")


@app.route("/wydarzenia")
def wydarzenia():
    return render_template("wydarzenia.html")


@app.route("/utworz-wydarzenie")
def utworz_wydarzenie():
    return render_template("utworz_wydarzenie.html")


@app.route("/zadania-do-rozdzielenia")
def zadania_do_rozdzielenia():
    return render_template("zadania_do_rozdzielenia.html")


@app.route("/zadania-przydzielone")
def zadania_przydzielone():
    return render_template("zadania_przydzielone.html")


if __name__ == "__main__":
    #engine = Engine()
    #engine.startEngine()
    app.run(debug=True)
