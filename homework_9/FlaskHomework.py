## Step 2 - Climate App
#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

## Hints
#* You will need to join the station and measurement tables for some of the analysis queries.
#* Use Flask `jsonify` to convert your API data into a valid JSON response object.

from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.pool import SingletonThreadPool

from flask import Flask, jsonify

import pymysql
import datetime as dt
import json

pymysql.install_as_MySQLdb()

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
session = Session(bind=engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station   

# Flask
app = Flask(__name__)

#* Use FLASK to create your routes.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;</br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

#* `/api/v1.0/precipitation`
#  * Query for the dates and precipitation observations from the last year.
#  * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
#  * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    dict = {}
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # Calculate the date one year from the last date in data set

    last_date = dt.datetime.strptime('2017-08-23', '%Y-%m-%d')
    prev_year = last_date - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    for row in results:
        if row[0] in dict:
            dict[row[0]] += "," + str(row[1])
        else:
            dict[row[0]] = str(row[1])
    return jsonify(dict) 

#* `/api/v1.0/tobs`
#  * Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    dict = {}
    last_date = dt.datetime.strptime('2017-08-23', '%Y-%m-%d')
    prev_year = last_date - dt.timedelta(days=365)
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()
    for row in temp_results:
        if row[0] in dict:
            dict[row[0]] += "," + str(row[1])
        else:
            dict[row[0]] = str(row[1])
    return jsonify(dict) 

#* `/api/v1.0/stations`
#  * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    return jsonify(results)


#* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature
#  for a given start or start-end range.
#  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<startdate>")
def temp_start(startdate):
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= startdate)
    min = temp_results[0][0]
    avg = temp_results[0][1]
    max = temp_results[0][2]
    
    return jsonify(min, avg, max)


#  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
     # for dates between the start and end date inclusive.
@app.route("/api/v1.0/<startdate>/<enddate>")
def temp_range(startdate, enddate):
    temp_range_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= startdate).filter(Measurement.date <= enddate)
    TMIN = temp_range_results[0][0]
    TAVG = temp_range_results[0][1]
    TMAX = temp_range_results[0][2]

    return jsonify(TMIN, TAVG, TMAX)

# With debug=True, Flask server will auto-reload when there are code changes
if __name__ == '__main__':
	app.run(debug=False)
