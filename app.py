import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine=engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/[YY-MM-DD]/[YY-MM-DD]<br/>"
        )

@app.route("/api/v1.0/precipitation")
def datestobs():
    """Return a list of dates and tobs data """
    # Query all measurements starting 2017-01-01
    Precepetation_data = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >="2017-01-01").\
    all()
    # Create a dictionary from the row data
    all_datestobs = []
    for result in Precepetation_data:
        result_dict = {}
        result_dict["date"] = result.date
        result_dict["tobs"] = result.tobs
        all_datestobs.append(result_dict)

    return jsonify(all_datestobs)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations data"""
    # Query all stations
    Stations_data = session.query(Station).all()
    # Create a dictionary from the row data
    all_stations = []
    for result in Stations_data:
        station_dict = {}
        station_dict["station"] = result.station
        station_dict["name"] = result.name
        station_dict["latitude"] = result.latitude
        station_dict["longitude"] = result.longitude
        station_dict["elevation"] = result.elevation       
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs data"""
    # Query all tobs
    tobs_data = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >="2017-01-01").\
    all()
    # Create a dictionary from the row data
    all_tobs = []
    for result in tobs_data:
        tobs_dict = {}
        tobs_dict["tobs"] = result.tobs
        all_tobs.append(tobs_dict)

@app.route("/api/v1.0/(start)")
def start(start_date):
    stats = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>start).all()
    start = list(np.ravel(stats))
    
    return(jsonify(start))

# @app.route("/api/v1.0/<start_date>/<end_date>")
# def start_end(start_date, end_date):
#     #Fetch the Tmin, Tmax, and Tavg when start and end date given""
#     sel = [func.max(Measurement.tobs), 
#            func.min(Measurement.tobs),
#            func.avg(Measurement.tobs)]

#     results = session.query(*sel).\
#     filter(func.strftime("%Y-%m-%D", Measurement.date) >= start_date).\
#     filter(func.strftime("%Y-%m-%D", Measurement.date) <= end_date).all()

#     return(jsonify(results))

if __name__ == '__main__':
    app.run(debug=True)
