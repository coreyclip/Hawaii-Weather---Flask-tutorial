# imports
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify,render_template

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measures = Base.classes.measures

# Create our session (link) from Python to the DB
session = Session(engine)



# Create an app, being sure to pass __name__
app = Flask(__name__)


# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
    f"Hawaii Weather Flask Tutorial:<br/>"
    f"Available Routes:<br/>"
    f"/about:<br/>"
    
    f"/api/v1.0/precipitation:<br/>"
    f"/api/v1.0/stations:<br/>"
    f"/api/v1.0/tobs:<br/>"
    f'/api/v1.0/<start>:<br/>'
    f"/api/v1.0/<start>/<end>:</br>")
    
    
# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "This is a simple demostration of connecting a \n SQL lite database to a web app"
    
    
@app.route("/api/v1.0/precipitation")
def prcp(year):
    results = session.query(measures.date, measures.prcp).\
    filter(func.strftime("%y", measures.date) == year).all()
    prcp_recs = []
    for rec in results:
        date_dict = {}
        date_dict['date'] = rec.prcp
        prcp_recs.append(date_dict)
    return jsonify(prcp_recs)
    
    
@app.route("/api/v1.0/stations")

def stations():
    """
    * Return a json list of stations from the dataset.
    """
    results = session.query(stations.name).all()
    records = list()
    for name in results:
        records.append(name)
        
    return jsonify(records)
    
@app.route("/api/v1.0/tobs")
def tobs(year):
    """
    Return a json list of Temperature Observations (tobs) for the previous year
    """
    results = session.query(measures.date, measures.tobs).\
        filter(func.strftime("%y", measures.date) == year).all()
    tobs_recs = []
    for rec in results:
        date_dict = {}
        date_dict['date'] = rec.tobs
        tobs_recs.append(date_dict)
    return jsonify(tobs_recs)
    
    
    
@app.route("/api/v1.0/<start>")
def calc_temp(start):
    results = session.query(measures.tobs).\
        filter(func.striftime(measures.date) > start).all()
    avg = np.mean(results)
    min_ = np.min(results)
    max_ = np.max(results)
    final_json = {	
                    "start_date":start,
                    "TMIN":min_,
                    "TAVG":avg,
                    "TMAX":max_
                }
    return jsonify(final_json)
        
        
@app.route("/api/v1.0/<start>/<end>")
def calc_temp_start_end(start,end):
    """

    * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

    * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    
    Arguments:
        start {[date]} -- [start date for a trip to Hawaii]
        end {[date]} -- [end date for a trip, must be after start]
    
    Returns:
        [json] -- [a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.]
    """

    results = session.query(measures.tobs).\
        filter(func.strftime(measures.date) < end).\
        filter(func.striftime(measures.date) > start).all()
    avg = np.mean(results)
    min_ = np.min(results)
    max_ = np.max(results)
    final_json = {	
                    "start_date":start,
                    "end_date":end,
                    "TMIN":min_,
                    "TAVG":avg,
                    "TMAX":max_
                }
    return jsonify(final_json)

if __name__ == "__main__":
    app.run(debug=True)

