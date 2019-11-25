from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# "postgres://yxklmagf:BMExbNgDuJewn8Gy109TrzgGDtPLNrh3@balarama.db.elephantsql.com:5432/yxklmagf")
# "postgres://postgres:@127.0.0.1:5432/kronika"


class DbConnection:
    engine = create_engine(
        "postgres://yxklmagf:BMExbNgDuJewn8Gy109TrzgGDtPLNrh3@balarama.db.elephantsql.com:5432/yxklmagf")
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Model = declarative_base(name='Model')
    Model.query = db_session.query_property()
