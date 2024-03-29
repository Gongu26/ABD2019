import time
from datetime import date

import sqlalchemy as db
from flask import session
from sqlalchemy import func

from db_connection import DbConnection
from models import Kronikarz, Zadanie, Kronikarz_Zadanie, Wniosek, Wydarzenie, Wydarzenie_Kronikarz

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

    def is_user_redaktor_naczelny(self, user_nr_indeksu):
        s = db.select([Kronikarz]).where(Kronikarz.nr_indeksu == user_nr_indeksu)

        result = dbConnection.engine.execute(s)
        kronikarz = result.fetchone()
        if kronikarz.rodzaj == "redaktor naczelny":
            return True
        return False

    def is_user_redaktor_organizacyjny(self, user_nr_indeksu):
        s = db.select([Kronikarz]).where(Kronikarz.nr_indeksu == user_nr_indeksu)

        result = dbConnection.engine.execute(s)
        kronikarz = result.fetchone()
        if kronikarz.rodzaj == "redaktor organizacyjny":
            return True
        return False

    def get_zadania_to_assign(self):
        result = dbConnection.db_session \
            .query(Zadanie) \
            .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania, isouter=True) \
            .filter(Kronikarz_Zadanie.id == None)

        return result.all()

    def get_aktualne_zadania_amount_by_user(self):
        result = dbConnection.db_session \
            .query(Kronikarz, func.count(Zadanie.id)) \
            .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania) \
            .join(Kronikarz, Kronikarz.nr_indeksu == Kronikarz_Zadanie.nr_indeksu_kronikarza) \
            .filter(Zadanie.wyznaczona_data_realizacji > date.today()) \
            .group_by(Kronikarz.nr_indeksu)

        return result.all()

    def get_zadania_by_user(self, user_nr_indeksu):
        result = dbConnection.db_session \
            .query(Zadanie) \
            .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania) \
            .join(Kronikarz, Kronikarz.nr_indeksu == Kronikarz_Zadanie.nr_indeksu_kronikarza) \
            .filter(Kronikarz.nr_indeksu == user_nr_indeksu)
        return result.all()

    def get_all_actual_wnioski(self):
        result = dbConnection.db_session \
            .query(Wniosek, Kronikarz) \
            .join(Kronikarz, Wniosek.nr_indeksu_kronikarza == Kronikarz.nr_indeksu) \
            .filter(Wniosek.data_rozpatrzenia == None) \
            .order_by(Wniosek.data_zlozenia)

        return result.all()

    def get_wnioski_by_user(self, user_nr_indeksu):
        result = dbConnection.db_session \
            .query(Wniosek, Kronikarz) \
            .join(Kronikarz, Wniosek.nr_indeksu_kronikarza == Kronikarz.nr_indeksu) \
            .filter(Kronikarz.nr_indeksu == user_nr_indeksu) \
            .order_by(Wniosek.data_zlozenia)

        return result.all()

    def get_wydarzenia_by_user(self, user_nr_indeksu):
        result = dbConnection.db_session \
            .query(Wydarzenie) \
            .join(Wydarzenie_Kronikarz, Wydarzenie.id == Wydarzenie_Kronikarz.id_wydarzenia) \
            .join(Kronikarz, Wydarzenie_Kronikarz.nr_indeksu_kronikarza == Kronikarz.nr_indeksu) \
            .filter(Kronikarz.nr_indeksu == user_nr_indeksu)
        return result.all()

    def add_wydarzenie(self, rodzaj, data, godz_rozp, godz_zako, opis):
        wydarzenie = Wydarzenie(rodzaj, data, godz_rozp, godz_zako, opis)
        dbConnection.db_session.add(wydarzenie)
        dbConnection.db_session.commit()

    def add_wniosek(self, rodzaj, tresc, nr_indeksu_kronikarza):
        if rodzaj == 'wypożyczenie sprzętu':
            rodzaj = 'wypoyczenie sprztu'
        wniosek = Wniosek(rodzaj=rodzaj,
                          data_zlozenia=date.today(),
                          czy_przyjeto=None,
                          data_rozpatrzenia=None,
                          tresc=tresc,
                          nr_indeksu_kronikarza=nr_indeksu_kronikarza)
        dbConnection.db_session.add(wniosek)
        dbConnection.db_session.commit()

    def accept_wniosek(self, wniosek_id):
        update = db.update(Wniosek) \
            .where(Wniosek.id == wniosek_id) \
            .values(dict(data_rozpatrzenia=date.today(), czy_przyjeto=True))
        dbConnection.engine.execute(update)

    def reject_wniosek(self, wniosek_id):
        update = db.update(Wniosek) \
            .where(Wniosek.id == wniosek_id) \
            .values(dict(data_rozpatrzenia=date.today(), czy_przyjeto=False))
        dbConnection.engine.execute(update)

    def match_kronikarze_zadanie(self, id_zadania, wyznaczona_data_realizacji, kronikarze):
        for i in range(0, len(kronikarze)):
            s = db.select([Kronikarz]).where(Kronikarz.email == kronikarze[i])

            result = dbConnection.engine.execute(s)
            kronikarz = result.fetchone()
            if kronikarz is not None:
                print(kronikarz.nr_indeksu)
                dbConnection.engine.begin()
                try:
                    # check if kronikarz assigned on that data
                    result = dbConnection.db_session \
                        .query(Zadanie) \
                        .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania) \
                        .filter(Kronikarz_Zadanie.nr_indeksu_kronikarza == kronikarz.nr_indeksu,
                                Zadanie.wyznaczona_data_realizacji == wyznaczona_data_realizacji)
                    r=result.all()
                    print(r)
                    if not r:
                        kronikarz_zadanie = Kronikarz_Zadanie(id_zadania, kronikarz.nr_indeksu)
                        dbConnection.db_session.add(kronikarz_zadanie)
                        print(kronikarz_zadanie.nr_indeksu_kronikarza)
                        time.sleep(15)
                        dbConnection.db_session.commit()
                        print('koniec')
                except:
                    dbConnection.db_session.abort()
                    raise
