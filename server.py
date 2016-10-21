from flask import Flask
from flask import request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Temperature, Base

app = Flask(__name__)
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

@app.route("/health-check")
def health_check():
    return "200"

@app.route("/temperature", methods=['POST'])
def temperature():
    temp = request.form['temp']
    session = DBSession()
    session.add(Temperature(temperature=temp))
    session.commit()
    return temp

if __name__ == '__main__':
    app.run(debug=True)
