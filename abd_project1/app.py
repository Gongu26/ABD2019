from flask import Flask, render_template
import os
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships, sessionmaker

app = Flask(__name__)

if os.path.exists('test.db'):
    os.remove('test.db')


db = create_engine('sqlite:///test.db')

BazaModel = declarative_base()


class Wniosek(BazaModel):
    __tablename__ = 'wniosek'
    id = Column(Integer, primary_key=True)
    nr_indeksu_kronikarza = Column(Integer, ForeignKey('kronikarz.nr_indeksu'))
    data_zlozenia = Column(Date)
    rodzaj = Column(Enum)
    czy_przyjeto = Column(Boolean)
    tresc = Column(String)
    data_rozpatrzenia = Column(Date)


class Kronikarz(BazaModel):
    __tablename__ = 'kronikarz'
    nr_indeksu = Column(Integer, primary_key=True)
    imie = Column(String)
    nazwisko = Column(String)
    email = Column(String)
    uczelnia = Column(String)
    wydzial = Column(String)
    kierunek = Column(String)
    rodzaj = Column(Enum)


class Wydarzenie_Kronikarz(BazaModel):
    __tablename__ = 'wydarzenie_kronikarz'
    id = Column(Integer, primary_key=True)
    nr_indeksu_kronikarz = Column(Integer, ForeignKey('kronikarz.nr_indeksu'))
    id_wydarzenia = Column(Integer, ForeignKey('wydarzenie.id'))


class Wydarzenie(BazaModel):
    __tablename__ = 'wydarzenie'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    rodzaj = Column(Enum)
    opis = Column(String)
    godzina_rozpoczenia = Column(Integer)
    godzina_zakonczenia = Column(Integer)


class Kronikarz_Zadanie(BazaModel):
    __tablename__ = 'kronikarz_zadanie'
    id = Column(Integer, primary_key=True)
    nr_indeksu_kronikarz = Column(Integer, ForeignKey('kronikarz.nr_indeksu'))
    id_zadania = Column(Integer, ForeignKey('zadanie.id'))


class Zadanie(BazaModel):
    __tablename__ = 'zadanie'
    id = Column(Integer, primary_key=True)
    rodzaj_zadania = Column(String)
    data_wstawienia = Column(Date)
    wyznaczona_data_realizacji = Column(Date)
    faktyczna_data_realizacji = Column(Date)
    czy_zaakceptowane = Column(Boolean)
    opis = Column(String)
    id_zlecenia = Column(Integer)


BazaModel.metadata.create_all(db)


@app.route("/")
def home():
    return render_template("profil.html")


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
    app.run(debug=True)
