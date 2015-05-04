import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (
    os.path.join(basedir, 'library.db')
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)
)

Base = declarative_base(engine)
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)

def clear_db(tables):
    import models
    connection = engine.connect()
    queries = []
    for table in tables:
        queries.append('DROP TABLE if exists %s' % table)
    map(connection.execute, queries)