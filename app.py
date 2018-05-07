# 1. import Flask
from flask import Flask, jsonify

## climate_analysis.ipynb
#dependencies
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
import datetime as dt

#Use SQLAlchemy create_engine to connect to your sqlite database.
#Use the engine and connection string to create a database called hawaii.sqlite.
engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(bind=engine)
conn = engine.connect()

#Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those
#classes called Station and Measurement.
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.stations



# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
    )
#########################################################################################


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""
#    * Query for the dates and precipitation observations from the last year.
#           * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#           * Return the json representation of your dictionary.
    end_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    dt_year  = int(end_date_str[:4])
    dt_month =  int(end_date_str[5:7])
    dt_day = int(end_date_str[8:10])
    end_date = dt.date(dt_year, dt_month, dt_day)
    start_date = end_date - dt.timedelta(days=365)

#Select only the date and prcp values
    measurement_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    year_totals = []
    for result in measurement_year:
        year = {}
        year["date"] = result[0]
        year["prcp"] = result[1]
        year_totals.append(year)

    return jsonify(year_totals)

#########################################################################################
@app.route("/api/v1.0/stations")
def stations():
    stations_all = session.query(Station.name, Station.station)
    stations_result = []
    for result in stations_all:
        row = {}
        row["name"] = result[0]
        row["station"] = result[1]
        stations_result.append(row)
    return jsonify(stations_result)

#########################################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for prior year"""
#    * Query for the dates and temperature observations from the last year.
#           * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
#           * Return the json representation of your dictionary.
    end_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    dt_year  = int(end_date_str[:4])
    dt_month =  int(end_date_str[5:7])
    dt_day = int(end_date_str[8:10])
    end_date = dt.date(dt_year, dt_month, dt_day)
    start_date = end_date - dt.timedelta(days=365)

    measurement_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
     	filter(Measurement.date <= end_date).all()
# Create a list of dicts with `date` and `tobs` as the keys and values
    year_totals = []
    for result in measurement_year:
        year = {}
        year["date"] = result[0]
        year["tobs"] = result[1]
        year_totals.append(year)

    return jsonify(year_totals)

#########################################################################################

if __name__ == "__main__":
    app.run(debug=True)
