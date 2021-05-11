from flask import Flask, render_template, request
import time
import csv
from alerts import *
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', districts=get_districts(), message="Please fill in your information and we will send you an email when a vaccine slot is available in your area")


@app.route("/create_alert", methods=['POST', 'GET'])
def create_alert():
    if request.method == 'POST':
        alert = Alert(request.form["Name"], request.form["Email"], request.form["Address"], request.form["Pin"], request.form["Distance"], request.form["District"])
        alert.save_alert()
        return render_template('index.html', message="Successfully created alert. We will send you an email when a slot is available. Thank you.", districts=get_districts())


def get_districts():
    districts = {}
    with open('static/districts.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            districts[row[1]] = row[0]

    return districts

if __name__ == "__main__":
    app.run()