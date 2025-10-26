from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = None
db_session = None
Base = declarative_base()


def init_db(app):
    global engine, db_session, Base
    engine = create_engine(app.config.get('DATABASE_URI'))
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    import app.models
    Base.metadata.create_all(bind=engine)