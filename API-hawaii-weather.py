import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# Flask set up
app = Flask(__name__)

# Set up Flask Routes

@app.route("/")
def welcome():
    """Welcome to Hawaii's weather history"""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >="2016-08-24").all()

    session.close()

        # Dictionary for the data
    precipitation_list = []

    for date, prcp in results1:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def station():
    results2 = session.query(Station.station).all()
        
    session.close()
        
    station_list =[]

    for station in results2:
        station_dict = {}
        station_dict["station"] = station
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp():
    results3 = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >="2016-08-24").all()

    session.close()

        # Dictionary for the data
    temp_list = []

    for station, date, tobs in results3:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    return jsonify(temp_list)




if __name__ == '__main__':
    app.run(debug=True)