"""The Flask App."""

from flask import Flask, json, jsonify, request, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import asyncio


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
    customers =  db.Customer.query(models.Customer).all()
    return customers

def dbUpdate(customer=None):
    if not customer: return
    try:
        db.session.merge(customer)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

# long running process for check user in either sanctions list or pep list
async def checkInList(list_file_name=None, customer_id=0):
    if list_file_name:
        customer = models.Customer.query.filter_by(id=int(customer_id)).first()
        if not customer: return False
        first_name = customer.first_name
        last_name = customer.last_name
        dob = customer.dob
        with open(list_file_name) as f:
            lines = f.readlines()
            for line in lines:
                print('Line: {}'.format(line))
                if first_name.lower() in line.lower() or last_name in line.lower():
                    #if user found on the list make them change to appropriate status
                    if list_file_name == "sanctionlists.txt":
                        customer.status = "SANCTION_LIST_FOUND-3"
                    if list_file_name == "peplist.txt":
                        customer.status = "PEP_LIST_FOUND-5"
                    dbUpdate(customer)
                await asyncio.sleep(10)
                return True
        # if customer is not found in specific list-update status and save and return False
        if list_file_name == "sanctionlists.txt":
            customer.status = "SANCTION_LIST_NOT_FOUND-4"
        if list_file_name == "peplist.txt":
            customer.status = "PEP_LIST_NOT_FOUND-6"
        dbUpdate(customer)
        return False
    return False



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

    # start long task here

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
            customer = models.Customer(first_name=str(first_name),last_name=str(last_name),\
                date_added=date.today(), dob=dob, monthly_income=float(monthly_income))
            db.session.add(customer)
            db.session.commit()  
            customers = refreshCustomerList()
            MESSAGE = "Customer has been added"
            # list check process here
            # AYSNC PROCESS HERE
            checkInList(list_file_name="sanctionslist.txt", customer_id=int(customer.id))
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
