import sqlalchemy as db
from flask import session

from db_connection import DbConnection
from models import Kronikarz, Zadanie, Kronikarz_Zadanie, Wniosek, Wydarzenie

dbConnection = DbConnection()


class DbAccess:
    def get_user_by_email(self, email):
        s = db.select([Kronikarz]).where(Kronikarz.email == email)

        result = dbConnection.engine.execute(s)
        kronikarz = result.fetchone()
        return kronikarz

    def get_user_data(self):
        s = db.select([Kronikarz]).where(Kronikarz.nr_indeksu == session['id'])

        result = dbConnection.engine.execute(s)
        return result.fetchone()

    def is_user_redaktor_naczelny(self):
        s = db.select([Kronikarz]).where(Kronikarz.nr_indeksu == session['id'])

        result = dbConnection.engine.execute(s)
        kronikarz = result.fetchone()
        if kronikarz.rodzaj == "redaktor naczelny":
            return True
        return False

    def get_zadania_to_assign(self):
        result = dbConnection.db_session\
            .query(Zadanie)\
            .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania, isouter=True)\
            .filter(Kronikarz_Zadanie.id == None)

        return result.all()

    def get_zadania_by_user(self, user_nr_indeksu):
        result = dbConnection.db_session \
            .query(Zadanie) \
            .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania) \
            .join(Kronikarz, Kronikarz.nr_indeksu == Kronikarz_Zadanie.nr_indeksu_kronikarza)\
            .filter(Kronikarz.nr_indeksu == user_nr_indeksu)
        return result.all()

    def get_all_actual_wnioski(self):
        result = dbConnection.db_session \
            .query(Wniosek, Kronikarz) \
            .join(Kronikarz, Wniosek.nr_indeksu_kronikarza == Kronikarz.nr_indeksu) \
            .filter(Wniosek.data_rozpatrzenia == None)

        return result.all()

    def get_wnioski_by_user(self, user_nr_indeksu):
        result = dbConnection.db_session \
            .query(Wniosek, Kronikarz) \
            .join(Kronikarz, Wniosek.nr_indeksu_kronikarza == Kronikarz.nr_indeksu) \
            .filter(Kronikarz.nr_indeksu == user_nr_indeksu)

        return result.all()

    def get_wydarzenia_by_user(self, user_nr_indeksu):
        result = dbConnection.db_session \
            .query(Wydarzenie) \
            .join(Kronikarz, Wydarzenie.nr_indeksu_kronikarza == Kronikarz.nr_indeksu) \
            .filter(Kronikarz.nr_indeksu == user_nr_indeksu)

        return result.all()

    def add_wydarzenie(self):
        pass

    def add_wniosek(self):
        pass

    def accept_wniosek(self, wniosek_id):
        pass

    def reject_wniosek(self, wniosek_id):
        pass

    def match_kronikarze_zadanie(self, zadanie, kronikarze):
        pass
