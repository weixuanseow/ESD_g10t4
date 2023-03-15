#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import sys
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/${db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cursor = db.cursor()

class Appointment(db.Model):
    __tablename__ = 'appointment_history'
    appt_datetime = db.Column('Appt_DateTime', db.DateTime, primary_key=True)
    patient_id = db.Column('Patient_ID', db.Integer, db.ForeignKey('patient.Patient_ID'), nullable=False, primary_key=True)
    diagnosis = db.Column('Diagnosis', db.String(255))

    patient = db.relationship('Patient', primaryjoin = 'Appointment.patient_id == Patient.patient_id', backref = 'appointment_history')
    
    def __init__(self, appt_datetime, patient_id, diagnosis):
        self.appt_datetime = appt_datetime
        self.patient_id = patient_id
        self.diagnosis = diagnosis

    def json(self):
        return {
            "appt_datetime": self.appt_datetime,
            "patient_id": self.patient_id,
            "diagnosis": self.diagnosis
        }


@app.route("/pharmacy/<string:appt_datetime>")
def find_by_appt(appt_datetime):
    appt = Appointment.query.filter_by(appt_datetime = appt_datetime).first()
    if book:
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# @app.route("/pharmacy", methods=['POST'])
# def receiveLog():
#     # Check if the request contains valid JSON
#     log = None
#     if request.is_json:
#         log = request.get_json()
#         processLog(log)
#         # reply to the HTTP request
#         return jsonify({"code": 200, "data": 'OK. Drug dispensed successfully.'}), 200 # return message; can be customized
#     else:
#         log = request.get_data()
#         print("Received an invalid log:")
#         print(log)
#         print()
#         return jsonify({"code": 400, "message": "Drug dispense unsuccessful. Input should be in JSON."}), 400 # Bad Request

# def processLog(order):
#     print("Recording a log:")
#     print(order)
#     print() # print a new line feed as a separator


# if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
#     print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
#     app.run(host='0.0.0.0', port=5003, debug=True)