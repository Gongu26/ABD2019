import sqlalchemy as db
from flask import session

from db_connection import DbConnection
from models import Kronikarz, Zadanie, Kronikarz_Zadanie

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

    def get_task_to_assign(self):
        result = dbConnection.db_session\
            .query(Zadanie, Kronikarz_Zadanie)\
            .join(Kronikarz_Zadanie, Zadanie.id == Kronikarz_Zadanie.id_zadania, isouter=True)\
            .filter(Kronikarz_Zadanie is None)

        return result.all()
