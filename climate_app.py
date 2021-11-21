# import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(results))

    return jsonify(prcp)

# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

# Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_observations = session.query(Measurement.station, Station.station, func.count(Measurement.station)).\
    filter(Measurement.station == Station.station).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
    # Query all tobs
    most_active_station = station_observations[0][1]

    results =session.query(Measurement.tobs).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date > query_date).all()

    session.close()

    tobs = list(np.ravel(results))

    return jsonify(tobs)

if __name__ == "__main__":
    app.run(debug=True)
