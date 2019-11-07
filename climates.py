# Imports
import datetime as datetime
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Routes
last_date = datetime.datetime.strptime("2017-08-23", "%Y-%m-%d")
days = 365
dates = [last_date - datetime.timedelta(days=x) for x in range(0, days)]

new_dates = []
for date in dates:
    new_date = date.strftime("%Y-%m-%d")
    new_dates.append(new_date)

@app.route("/api/v1.0/precipitation")
def precipitation():
    dates_prcp = session.query(Measurement).filter(Measurement.date.in_(new_dates))
    prcp_data = []
    for day in dates_prcp:
        prcp_dict = {}
        prcp_dict[day.date] = day.prcp
        prcp_data.append(prcp_dict)
        
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station)
    station_data = []
    for stat in station:
        stat_dict = {}
        stat_dict['Station'] = stat.station
        stat_dict['Name'] = stat.name
        station_data.append(stat_dict)
        
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    tobsss = session.query(Measurement).filter(Measurement.date.in_(str_dates))
    tob_data = []
    for tob in tobsss:
        tob_dict = {}
        tob_dict[tob.date] = tob.tobs
        tob_data.append(tob_dict)
        
    return jsonify(tob_data)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    s_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    e_date = datetime.datetime.strptime("2017-08-23", "%Y-%m-%d")
    
    change = e_date - s_date
    dates = []
    for x in range(change.days + 1):
        dates.append(s_date + timedelta(days=x))
        
    str_dates = []
    for date in dates:
        n = date.strftime("%Y-%m-%d")
        str_dates.append(n)
        
    average_temp = session.query(func.avg(Measurement.tobs)).\
                filter(Measurement.date.in_(str_dates))[0][0]
    minimum_temp = session.query(func.min(Measurement.tobs)).\
                filter(Measurement.date.in_(str_dates))[0][0]
    maximum_temp = session.query(func.max(Measurement.tobs)).\
                filter(Measurement.date.in_(str_dates))[0][0]
        
    temp_dict = {}
    temp_dict['Average Temperature'] = average_temp
    temp_dict['Minimum Temperature'] = minimum_temp
    temp_dict['Maximum Temperature'] = maximum_temp
    
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    s_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    e_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    
    change = e_date - s_date
    dates = []
    for x in range(change.days + 1):
        dates.append(s_date + timedelta(days=x))
        
    str_dates = []
    for date in dates:
        n = date.strftime("%Y-%m-%d")
        str_dates.append(n)
        
    average_temp = session.query(func.avg(Measurement.tobs)).\
                filter(Measurement.date.in_(str_dates))[0][0]
    minimum_temp = session.query(func.min(Measurement.tobs)).\
                filter(Measurement.date.in_(str_dates))[0][0]
    maximum_temp = session.query(func.max(Measurement.tobs)).\
                filter(Measurement.date.in_(str_dates))[0][0]
        
    temp_dict = {}
    temp_dict['Average Temperature'] = average_temp
    temp_dict['Minimum Temperature'] = minimum_temp
    temp_dict['Maximum Temperature'] = maximum_temp
    
    return jsonify(temp_dict)

if __name__ == "__main__":
   app.run(debug=True)