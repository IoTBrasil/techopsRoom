from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

import math
import statistics
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
import logging
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

def averageCalculator(list):
    sum = 0
    for number in list:
        sum += number

    return sum/len(list)

def standardDeviationCalculator(average,list):
   return statistics.pstdev(list)

@app.route('/temperature', methods=['GET'])
def temperatureControl():
    temperature = "0"
    time = '0:00:00'
    session = DBSession()
    temperatures= []
    lines =  session.query(Temperature).order_by(Temperature.time.desc()).limit(5).all()
    reversedList = list(reversed(lines))
    for row in reversedList:
        temperature = temperature + "," +  str(row.temperature) 
        time = time + ',' +  str(row.time.time()).split('.',1)[0] 
        temperatures.append(row.temperature)

    average =  averageCalculator(temperatures) 
    standardDeviation = standardDeviationCalculator(average,temperatures)
    return render_template('temperature.html', temperature=temperature,
            time=time.split(','), average = average,standardDeviation =
            standardDeviation) 

@app.route("/temperature", methods=['POST'])
def temperature():
    json = request.get_json()
    temp = json['temp']
    print " Temperature "+ str(temp)
    session = DBSession()
    temperature = Temperature(temperature=temp, time=datetime.now())
    session.add(temperature)
    session.commit()
    return str(temp) 




def dumpTemperatureTable():
    time = datetime.now() + timedelta(days =-1) 
    session = DBSession()
    session.query(Temperature).filter(time >= Temperature.time).delete()
    session.commit()
    print str(time)
    return str(time)
    

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(dumpTemperatureTable, 'interval', days=1)
    scheduler.start()
    logging.basicConfig()
    app.run(debug=True)

