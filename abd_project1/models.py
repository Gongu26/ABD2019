import sqlalchemy as db

from dbConnection import DbConnection

dbConnection = DbConnection()

kronikarz = db.Table('kronikarz', db.MetaData(), autoload=True, autoload_with=dbConnection.engine)
