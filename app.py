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
Samples_Metadata= Base.classes.samples_metadata

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

#################################################
# Returns a list of sample names
@app.route('/names')
def names():

    # Create an empty list for sample ids
    sample_ids = []

    # Query results from matadata table
    results = session.query(Samples_Metadata.SAMPLEID)

    # Loop through the query results and append the list with sample ids
    for result in results:
        sample_ids.append("BB_" + str(result[0]))
        
    return jsonify(sample_ids)

#################################################
# Returns a list of OTU descriptions 
@app.route('/otu')
def otu():

    # Create an empty list for otu description
    otu_desc = []

    # Query results from otu table
    results = session.query(Otu.lowest_taxonomic_unit_found)

    # Loop through the query results and append the list with otu description
    for result in results:
        otu_desc.append(result[0])
        
    return jsonify(otu_desc)

#################################################
# Returns a json dictionary of sample metadata 
@app.route('/metadata/<sample>')
def metadata(sample):
    sample = sample.replace("BB_","")

    metadata = session.query(Samples_Metadata.AGE, Samples_Metadata.BBTYPE, Samples_Metadata.ETHNICITY, Samples_Metadata.GENDER, Samples_Metadata.LOCATION, Samples_Metadata.SAMPLEID).filter_by(SAMPLEID=sample).first()
    metadict = {"AGE":metadata[0],"BBTYPE":metadata[1],"ETHNICITY":metadata[2], "GENDER":metadata[3],"LOCATION":metadata[4],"SAMPLEID":metadata[5]}
    return jsonify(metadict)

#################################################
# Returns an integer value for the weekly washing frequency `WFREQ`
@app.route('/wfreq/<sample>')
def wfreq(sample):
    sample = sample.replace("BB_","")

    # Query from metadata table
    wfreq = session.query(Samples_Metadata.WFREQ).filter_by(SAMPLEID = sample).scalar()

    return str(wfreq)

#################################################
# Return a list of dictionaries containing sorted lists  for `otu_ids`and `sample_values`
@app.route('/samples/<sample>')
def samples(sample):

    # Create sample query
    sample_query = "Samples." + sample

    # Create empty dictionary & lists
    samples_info = {}
    otu_ids = []
    sample_values = []

    # Grab info
    results = session.query(Samples.otu_id, sample_query).order_by(desc(sample_query))

    # Loop through & append
    for result in results:
        otu_ids.append(result[0])
        sample_values.append(result[1])

    # Add to dictionary
    samples_info = {
        "otu_ids": otu_ids,
        "sample_values": sample_values
    }

    return jsonify(samples_info)

if __name__ == "__main__":
    app.run(debug=True)