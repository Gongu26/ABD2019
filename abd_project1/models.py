import sqlalchemy as db
from sqlalchemy import Sequence

from db_connection import DbConnection

dbConnection = DbConnection()


class Kronikarz(dbConnection.Model):
    __tablename__ = 'kronikarz'
    nr_indeksu = db.Column('nr_indeksu', db.String(6), primary_key=True)
    imie = db.Column('imie',db.String(15))
    nazwisko = db.Column('nazwisko', db.String(20))
    email = db.Column('email', db.String(35))
    haslo = db.Column('haslo', db.String(15))
    uczelnia = db.Column('uczelnia', db.String(40))
    wydzial = db.Column('wydzial', db.String(40))
    kierunek = db.Column('kierunek', db.String(40))
    rodzaj = db.Column('rodzaj', db.String(40))

    def __init__(self, nr_indeksu, imie, nazwisko, email, haslo, uczlenia, wydzial, kierunek, rodzaj):
        self.nr_indeksu = nr_indeksu
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.haslo = haslo
        self.uczlenia = uczlenia
        self.wydzial = wydzial
        self.kierunek = kierunek
        self.rodzaj = rodzaj

    def __eq__(self, other):
        if self.nr_indeksu is None:
            if other is None:
                return True
        return type(self) is type(other) and self.nr_indeksu == other.nr_indeksu

    def __ne__(self, other):
        return not self.__eq__(other)


class Wniosek(dbConnection.Model):
    __tablename__ = 'wniosek'
    id = db.Column(db.Integer, Sequence('wniosek_id_seq', start=4, increment=1), primary_key=True)
    data_zlozenia = db.Column(db.Date)
    rodzaj = db.Column(db.String)
    czy_przyjeto = db.Column(db.Boolean)
    tresc = db.Column(db.String)
    data_rozpatrzenia = db.Column(db.Date)
    nr_indeksu_kronikarza = db.Column(db.Integer, db.ForeignKey('kronikarz.nr_indeksu'))

    def __init__(self, data_zlozenia, rodzaj, czy_przyjeto, tresc, data_rozpatrzenia, nr_indeksu_kronikarza):
        self.data_zlozenia = data_zlozenia
        self.rodzaj = rodzaj
        self.czy_przyjeto = czy_przyjeto
        self.tresc = tresc
        self.data_rozpatrzenia = data_rozpatrzenia
        self.nr_indeksu_kronikarza = nr_indeksu_kronikarza


class Wydarzenie_Kronikarz(dbConnection.Model):
    __tablename__ = 'wydarzenie_kronikarz'
    id = db.Column(db.Integer, primary_key=True)
    nr_indeksu_kronikarza = db.Column(db.Integer, db.ForeignKey('kronikarz.nr_indeksu'))
    id_wydarzenia = db.Column(db.Integer, db.ForeignKey('wydarzenie.id'))

    def __init__(self, id_wydarzenia, nr_indeksu_kronikarza):
        self.id_wydarzenia = id_wydarzenia
        self.nr_indeksu_kronikarza = nr_indeksu_kronikarza


class Wydarzenie(dbConnection.Model):
    __tablename__ = 'wydarzenie'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    rodzaj = db.Column(db.String)
    opis = db.Column(db.String)
    godzina_rozpoczecia = db.Column(db.TIMESTAMP)
    godzina_zakonczenia = db.Column(db.TIMESTAMP)

    def __init__(self, rodzaj, data, godzina_rozpoczenia, godzina_zakonczenia, opis):
        self.data = data
        self.rodzaj = rodzaj
        self.opis = opis
        self.godzina_rozpoczenia = godzina_rozpoczenia
        self.godzina_zakonczenia = godzina_zakonczenia


class Kronikarz_Zadanie(dbConnection.Model):
    __tablename__ = 'kronikarz_zadanie'
    id = db.Column(db.Integer, primary_key=True)
    nr_indeksu_kronikarza = db.Column(db.Integer, db.ForeignKey('kronikarz.nr_indeksu'))
    id_zadania = db.Column(db.Integer, db.ForeignKey('zadanie.id'))

    def __init__(self, id_zadania, nr_indeksu_kronikarza):
        self.id_zadania = id_zadania
        self.nr_indeksu_kronikarza = nr_indeksu_kronikarza


class Zadanie(dbConnection.Model):
    __tablename__ = 'zadanie'
    id = db.Column(db.Integer, primary_key=True)
    rodzaj_zadania = db.Column(db.String)
    data_wstawienia = db.Column(db.Date)
    wyznaczona_data_realizacji = db.Column(db.Date)
    faktyczna_data_realizacji = db.Column(db.Date)
    czy_zaakceptowane = db.Column(db.Boolean)
    opis = db.Column(db.String)

    def __init__(self, id, rodzaj_zadania, data_wstawienia, wyznaczona_data_realizacji, faktyczna_data_realizacji,
                 czy_zaakceptowane, opis):
        self.id = id
        self.rodzaj_zadania = rodzaj_zadania
        self.data_wstawienia = data_wstawienia
        self.wyznaczona_data_realizacji = wyznaczona_data_realizacji
        self.faktyczna_data_realizacji = faktyczna_data_realizacji
        self.czy_zaakceptowane = czy_zaakceptowane
        self.opis = opis
