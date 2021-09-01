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

@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404
@app.route("/".format(API_VERSION))
def index():
    customers =  db.session.query(models.Customer).all()
    # update/format status field
    for c in customers:
        c.status = "({}-{})".format(c.status,models.STATUS[c.status])
    return render_template("index.html", customers=customers)

@app.route("/{}/add-customer".format(API_VERSION), methods=["POST"])
def add_customer():
    """Receives Customer Information and Adds it to Database"""
    print('on added customer')
    try:
        first_name = request.form.get('first_name', None)
        last_name = request.form.get('last_name', None)
        dob = request.form.get('dob', None)
        from datetime import datetime
        dob = datetime.strptime(dob, '%Y-%m-%d')
        monthly_income = request.form.get('monthly_income', 0)
        if first_name and last_name and dob and monthly_income:
            custom_information = models.Customer(first_name=str(first_name),last_name=str(last_name),\
                date_added=date.today(), dob=dob, monthly_income=float(monthly_income))
            db.session.add(custom_information)
            db.session.commit()   
            customers =  db.session.query(models.Customer).all()
            for c in customers:
                c.status = "({}-{})".format(c.status,models.STATUS[c.status])

            return redirect(url_for('index', customers=customers, message="Customer has been Added"))
        else:
            return jsonify(
                message="Failed to Add Customer",
                first_name=first_name,
                status = str(200)
            )
    except Exception as e:
        print(e)
        return jsonify(
        message = "Exception:{}".format(str(e)),
        customers = [],
        count = 0,
        status = str(500)

    )


@app.route("/{}/all-customers".format(API_VERSION), methods=["GET"])
def all_customers():
    """Return All Customers"""
    try:
            customers =  db.session.query(models.Customer).all()
            return jsonify(
            message= "Customers Found!",
            customers=[i.serialize for i in customers],
            count = len(customers),
            status = str(200)
        )
    except Exception as e:
        return jsonify(
            message = "Exception:{}".format(str(e)),
            customers = [],
            count = 0,
            status = str(200)
        )

# @app.route("/{}/search-item".format(API_VERSION), methods=["POST"])
# def search_items():
#     """Search for Item"""
#     try:
#         data = request.json

#         if not data:
#             data = request.form

#         search_primer =  data.get("search_primer", None)
#         if not search_primer: return jsonify(message="No Items Found!",
#         items=[]
#         )

#         list_items =  db.session.query(models.ListItem).all()
#         if list_items:
#             # filter items based on search key
#             list_items = [
#                 i.serialize for i in list_items if search_primer in str(
#                     i.serialize.get("name", ""))
#             ]
            
#         return jsonify(
#         message = "Items Found!" if len(list_items)>0 else "No Items Found",
#         items=[i for i in list_items
#         ],
#         count = len(list_items),
#         status = str(200),
#         )
#     except Exception as e:
#         return jsonify(
#             message = "Exception:{}".format(str(e)),
#             count = 0,
#             items =[],
#             status = str(500)
#         )

if __name__ == "__main__":
  
    app.run(host='0.0.0.0', debug=True, port=5000)
