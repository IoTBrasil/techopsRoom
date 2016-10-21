import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from datetime import datetime

Base = declarative_base()

class Temperature(Base):
    __tablename__ = 'temperature'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    temperature = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.utcnow)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///database.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
