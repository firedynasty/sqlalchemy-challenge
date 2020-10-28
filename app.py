from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

app = Flask(__name__)

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()

Base.prepare(engine, reflect=True)

session = Session(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station


@app.route('/')

def index():
	return(
		f"Welcome to the Page!<br/>"
		f"Avaiable Routes:<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/Date-in-%Y-%m-%d<br/>"
		f"example:<br/>"
		f"/api/v1.0/2012-03-13<br/>"
		f"/api/v1.0/start_date/end_date"
		)


@app.route("/api/v1.0/precipitation")

def precipitation_go():
	results = session.query(Measurement.date, Measurement.prcp).all()
	return jsonify(results)

@app.route("/api/v1.0/stations")

def station_go():
	results = session.query(Station.name).all()
	return jsonify(results)

@app.route("/api/v1.0/tobs")

def station_date():
	query_date = dt.date(2016,8,18)
	selection = [Measurement.date, Measurement.station, Measurement.tobs]
	last_12_months = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date > query_date).filter(Measurement.station == 'USC00519281').all()
	return jsonify(last_12_months)


@app.route("/api/v1.0/<start>")
def start_date(start):
	results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
	return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_and_date(start, end):
	results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	return jsonify(results)
