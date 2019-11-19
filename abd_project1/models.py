import sqlalchemy as db


class Kronikarz (db.Model):
    nr_indeksu = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.string(15))
    nazwisko = db.Column(db.string(20))
    email = db.Column(db.string(35))
    haslo = db.Column(db.string(15))
    uczelnia = db.Column(db.string(40))
    wydzial = db.Column(db.string(40))
    kierunek = db.Column(db.string(40))
    rodzaj = db.Column(db.string)
