# 
#### Documentation
#
## Flask
#
# https://www.quora.com/Who-is-behind-Flask-and-what-is-the-story-of-its-creation # History of Flask
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#WSGI-compatible_applications_and_frameworks
# https://meyerweb.com/eric/tools/dencoder/
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# https://github.com/lerocha/chinook-database
# https://realpython.com/primer-on-python-decorators/
#
## SQLAlchemy
#
# https://www.sqlalchemy.org/features.html
# https://docs.sqlalchemy.org/en/13/dialects/
# https://docs.sqlalchemy.org/en/13/orm/extensions/automap.html
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html
# https://www.w3schools.com/sql/sql_injection.asp
# https://numpy.org/doc/stable/reference/generated/numpy.ravel.html
# https://sqlite.org/lang_datefunc.html
#
## Authentification - JWT Token (Not use in this module)
#
# https://bezkoder.com/react-hooks-jwt-auth/
#
### Kernel Setup
#
# PythonData Kernel: conda activate PythonData && pip install datetime (if missing)
# 
### FLASK & JSONIFY https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify 
# 
from flask import Flask, jsonify

# Python Packages - GENERAL DEPENDENCIES
import datetime as dt 
import numpy as np
import pandas as pd
import sys

# SQL
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# CONNECTION SQL
engine = create_engine("sqlite:///hawaii.sqlite") # In order to connect to our SQLite database
session = Session(engine) # Session SQL - SQLAlchemy Session to query our database

Base = automap_base() # Automap Base creates a base class for an automap schema in SQLAlchemy 
Base.prepare(engine, reflect=True) # we'll reflect the schema of our SQLite tables into our code and create mappings
Base.classes.keys() # Confirm that the Automap was able to find all of the data in the SQLite database

# Key variables - Specific class
Measurement = Base.classes.measurement # Storage for Measurement
Station = Base.classes.station # Storage for Station


# Import app
app = Flask(__name__)
#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
#    print("example is being run directly.")
#else:
#    print("example is being imported")

# Routes HOME /
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# ROUTES Precipitation
# .\ to continue the query on the line below
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# ROUTES Station
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# ROUTES temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# ROUTES for statistics
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Code correction from Slack #class-2 - START
    if not end:
     results = session.query(*sel).\
            filter(Measurement.date >= start).all()
     temps = list(np.ravel(results))
     return jsonify(temps)
     # Code correction from Slack #class-2 - END

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)