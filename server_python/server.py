from flask import Flask
from flask import request
from flask import render_template
from datetime import datetime

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

@app.route('/index')
def root():
     return app.send_static_file('index.html')

@app.route('/temperature')
def temperatureControl():
    temperature = "0"
    time = '0:00:00'
    session = DBSession()
    for row in session.query(Temperature).all():
        temperature = temperature + "," +  str(row.temperature) 
        time = time + ',' +  str(row.time.time()).split('.',1)[0] 
    return render_template('temperature.html', temperature=temperature,
            time=time.split(',')) 

@app.route("/temperature-1", methods=['POST'])
def temperature():
    temp = request.form['temp']
    print " Temperature "+ temp
    session = DBSession()
    session.add(Temperature(temperature=temp, time=datetime.now()))
    session.commit()
    return temp

if __name__ == '__main__':
    app.run(debug=True)

