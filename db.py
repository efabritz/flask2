import atexit

from sqlalchemy import Column, String, Integer, DateTime, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = "postgresql://postgres:postgres@127.0.0.1:5432/flask_db"

engine = create_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)

    ads = relationship('Advertisement', backref='user')

    def __repr__(self):
        return f'<User "{self.username}">'

class Advertisement(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'<Advertisement "{self.header[:10]}...">'

Base.metadata.create_all(bind=engine)