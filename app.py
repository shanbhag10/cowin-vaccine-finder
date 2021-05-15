from flask import Flask, render_template, request
import time
import csv
from alerts import *
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    message = "Please fill in your information and you will receive email alerts whenever a vaccine slot becomes available in your area. (Every 15min) <br />"
    return render_template('index.html', districts=get_districts(), message=message, message_color="#006bb3")


@app.route("/create_alert", methods=['POST', 'GET'])
def create_alert():
    if request.method == 'POST':
        alert = Alert(request.form["Name"], request.form["Email"], request.form["Address"], request.form["Pin"], request.form["Distance"], request.form["District"])
        response = alert.save_alert()

        if response is not None:
            return render_template('index.html', message=response, districts=get_districts(), message_color="red")

        return render_template('success.html')


@app.route("/unsubscribe/<email>", methods=['POST', 'GET'])
def unsubscribe(email):
    if request.method == 'GET':
        delete_alert(email)
        return render_template('unsubscribe.html')


def get_districts():
    districts = {}
    with open('static/districts.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            districts[row[1]] = row[0]

    return districts

if __name__ == "__main__":
    app.run()