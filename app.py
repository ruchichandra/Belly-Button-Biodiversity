# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify, render_template, request
import csv

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_metdat = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Returns the dashboard homepage
@app.route("/")
def home():
    return render_template("index.html")

# Returns a list of sample names
@app.route('/names')
def names():

    # Create an empty list for sample ids
    sample_ids = []

    # Query results from matadata table
    results = session.query(Samples_Metadata.SAMPLED)

    # Loop through the query results and append the list with sample ids
    for result in results:
        sample_ids.append("BB_" + str(result[0]))
        
    return jsonify(sample_ids)

   


if __name__ == "__main__":
    app.run(debug=True)