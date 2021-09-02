"""SQLAlchemy database models."""
import datetime


from flask_migrate import Migrate
from flask import Flask

from sqlalchemy import Column, Integer, String, DateTime, Float
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import FLOAT, DateTime

from .database import DATABASE_URL



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

STATUS = {
    "APPROVED": 1,
    "DENIED" : 2,
    "SANCTION_APPROVED":3,
    "SANCTION_DENIED": 4,
    "PEP_APPROVED": 5,
    "PEP_DENIED": 6,
    "PENDING": 7
}

class Customer(db.Model):
    """Customer Information Model"""
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(1000), index=True)
    last_name = Column(String(1000), index=True)
    monthly_income = Column(Float)
    dob = Column(DateTime)
    date_added = Column(DateTime)
    status = Column(String(1000), default="PENDING-7")

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id' : self.id,
           'name': self.name,
           'date_added': dump_datetime(self.date_added),
       }


db.create_all()
