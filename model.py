import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Countries(Base):
    __tablename__ = 'countries'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    code = Column(String(3))
    name = Column(String(250))
    records = relationship('Records', backref='records')


class Records(Base):
    __tablename__ = 'records'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)

    # 6X0  600 or 610
    # 008
    year_pub = Column(String(5))
    language = Column(String(3))
    country = Column(Integer, ForeignKey('countries.id'))
    # country = relationship('Countries', backref='countries')

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
