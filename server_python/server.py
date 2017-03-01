from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

import math
import statistics
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

def average(list):
    sum = 0
    for number in list:
        sum += number

    return sum/len(list)

def standardDeviation(average,list):
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

    average2 = average(temperatures) 
    sd = standardDeviation(average2,temperatures)
    return render_template('temperature.html', temperature=temperature,
            time=time.split(','), average = average2,standardDeviation = sd) 

@app.route("/temperature", methods=['POST'])
def temperature():
    json = request.get_json()
    temp = json['temp']
    print " Temperature "+ str(temp)
    session = DBSession()
    session.add(Temperature(temperature=temp, time=datetime.now()))
    session.commit()
    return str(temp) 

if __name__ == '__main__':
    app.run(debug=True)

