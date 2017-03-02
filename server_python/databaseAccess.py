from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Temperature, Base

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def retrieveTemperatureOrderByDesc():
    session = DBSession()
    return  session.query(Temperature).order_by(Temperature.time.desc()).limit(5).all()

def saveTemperature(temperature):
    session = DBSession()
    session.add(temperature)
    session.commit()

def deleteByTime(time):
    session = DBSession()
    session.query(Temperature).filter(time >= Temperature.time).delete()
    session.commit()




