# Import the dependencies.
# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import pandas as pd

engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)
Base = automap_base()
Base.prepare(autoload_with = engine)
Base.classes.keys()

Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Database Setup
#################################################
app = Flask(__name__)


@app.route('/')
def homepage():
    
     return (
        "Welcome to the Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/yyyy-mm-dd (Specify a start date)<br/>"
        "/api/v1.0/yyyy-mm-dd/yyyy-mm-dd (Specify a start and end date)"
    )
     
     
@app.route('/api/v1.0/precipitation')
def precipitation():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) -dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= query_date)\
    .all()
    
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)
    
@app.route('/api/v1.0/stations')
def stations():
    total_stations = session.query(func.count(Station.station)).scalar()
    station_activity = session.query(Measurement.station, func.count(Measurement.station))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc())\
    .first()
    
    return jsonify(stations)
    

@app.route('/api/v1.0/tobs')
def tobs():
    most_active_station_id = 'USC00519281'
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) -dt.timedelta(days=365)
    station_activity = session.query(Measurement.station, func.count(Measurement.station)) \
    .group_by(Measurement.station) \
    .order_by(func.count(Measurement.station).desc()) \
    .all()
    most_active_station = station_activity[0]
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station == most_active_station)\
    .filter(Measurement.date >= query_date)\
    .all()
    temperature_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
    .filter(Measurement.station == most_active_station_id) \
    .all()
    
    return jsonify(tobs_data)
    
    
@app.route('/api/v1.0/<start>')
def temperature_by_start(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
        .filter(Measurement.date >= start_date) \
        .all()
    
    temperature_response = {
        "TMIN": temperature_data[0][0],
        "TAVG": temperature_data[0][1],
        "TMAX": temperature_data[0][2]
    }
    
    return jsonify(temperature_response)
    
    
@app.route('/api/v1.0/<start>/<end>')
def temperature_by_start_end(start, end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    temperature_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)) \
        .filter(Measurement.date >= start_date) \
        .filter(Measurement.date <= end_date) \
        .all()
        
    temperature_response = {
        "TMIN": temperature_data[0][0],
        "TAVG": temperature_data[0][1],
        "TMAX": temperature_data[0][2]
    }

    return jsonify(temperature_response)
    
    




# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///sql_hawaii_url")

if __name__ == '__main__':
    app.run(debug=True)
