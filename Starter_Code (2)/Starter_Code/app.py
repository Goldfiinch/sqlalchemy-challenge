# Import the dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create session
session = Session(engine)

# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def homepage():

    """List all available API routes."""
    return (
        "<b>SURFSUP!! THE CLIMATE APP API</b><br/><br/>"
        "Available Routes:<br/><br/>"
        "<b>Precipitation Data</b><br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "<b>List of Stations</b><br/>"
        "/api/v1.0/stations<br/><br/>"
        "<b>Temperature Data of the Most Active Station</b><br/>"
        "/api/v1.0/tobs<br/><br/>"
        "<b>Temperature Data on Specific Date</b><br/>"
        "/api/v1.0/temp/YYYY-MM-DD<br/>"
        "/api/v1.0/temp/YYYY-MM-DD(Start)/YYYY-MM-DD(End)"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():

    # Calculate the year prior to the last date
    begin_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Selects the "date" and "prcp" columns from the "Measurement" table and filter the data 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= begin_date).order_by(Measurement.date).all()

    # Create a dictionary where the date is the key and the precipitation is the value 
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {
            date : prcp # tutor revision
        }
        precipitation.append(precipitation_dict)
    
    session.close()

    return jsonify(precipitation)


@app.route('/api/v1.0/stations')
def stations():

    # Query station data
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Create a list of dictionaries representing stations
    station_data = [{
        "Station": station, 
        "Name": name,
        "Latitude": latitude,
        "Longitude": longitude,
        "Elevation": elevation
    } for station, name, latitude, longitude, elevation in results]

    session.close()

    return jsonify(station_data)