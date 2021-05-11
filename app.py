from flask import Flask, render_template, request
import time
import csv
from alerts import *
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    message = "Please fill in your information and we will send you an email when a vaccine slot is available in your area. <br />Providing address and the distance you can travel will result in more accurate alerts. <br />Only one alert is allowed per email."
    return render_template('index.html', districts=get_districts(), message=message, message_color="#006bb3")


@app.route("/create_alert", methods=['POST', 'GET'])
def create_alert():
    if request.method == 'POST':
        alert = Alert(request.form["Name"], request.form["Email"], request.form["Address"], request.form["Pin"], request.form["Distance"], request.form["District"])
        response = alert.save_alert()

        message_color = "green" if response[0] == 201 else "red"

        return render_template('index.html', message=response[1], districts=get_districts(), message_color=message_color)


def get_districts():
    districts = {}
    with open('static/districts.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            districts[row[1]] = row[0]

    return districts

if __name__ == "__main__":
    app.run()