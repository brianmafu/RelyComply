"""The Flask App."""

from flask import Flask, json, jsonify, request, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from datetime import date

from . import models
from .database import DATABASE_URL

import os

API_VERSION = "v1"
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] =  DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

MESSAGE =""


def refreshCustomerList():
    customers =  db.session.query(models.Customer).all()
    return customers


@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404

@app.route("/".format(API_VERSION))
def index():

    customers = refreshCustomerList()
    return render_template("index.html", customers=customers, message=MESSAGE)



@app.route("/{}/decline-or-approve".format(API_VERSION), methods=["POST"])
def decline_or_approved_customer():
    action = request.json.get("action").title()
    id = request.json.get("id")
    try:
        customer = models.Customer.query.filter_by(id=id).first()
        if action == "Approved":
            customer.status = "APPROVED-1"
        if action == "Declined":
            customer.status = "DECLINED-2"
        try:
            db.session.merge(customer)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    except Exception as e:
        print(e)
    customers = refreshCustomerList()
    return render_template("index.html", customers=customers,  message="Customer has been Added")


@app.route("/{}/add-customer".format(API_VERSION), methods=["POST", "GET"])
def add_customer():
    """Saves customer information to database"""

    global MESSAGE
    if request.method == "GET":
        return redirect(url_for("index"))
    
    
    customers = refreshCustomerList()
    try:
        first_name = request.form.get('first_name', None)
        last_name = request.form.get('last_name', None)
        dob = request.form.get('dob', None)
        from datetime import datetime
        # format date
        dob = datetime.strptime(dob, '%Y-%m-%d')
        monthly_income = request.form.get('monthly_income', 0)
        if first_name and last_name and dob and monthly_income:
            custom_information = models.Customer(first_name=str(first_name),last_name=str(last_name),\
                date_added=date.today(), dob=dob, monthly_income=float(monthly_income))
            db.session.add(custom_information)
            db.session.commit()  
            customers = refreshCustomerList()
            MESSAGE = "Customer has been added"
            return redirect(url_for('index'))

        else:
            MESSAGE = "Failed to Add Customer"
            return render_template("index.html", customers=customers,  message="Failed to Add Customer")

    except Exception as e:
        if "time data" in str(e):
            MESSAGE = "EXCEPTION: Date of Birth Not Selected"
        return redirect(url_for('index'))


 

if __name__ == "__main__":
  
    app.run(host='0.0.0.0', debug=True, port=5000)
