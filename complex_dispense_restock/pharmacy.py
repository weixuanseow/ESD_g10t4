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

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column('Patient_ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Patient_Full_Name', db.String(255), nullable=False)
    date_of_birth = db.Column('Date_Of_Birth', db.Date, nullable=False)
    gender = db.Column('Gender', db.Enum('male', 'female', 'other'), nullable=False)
    phone = db.Column('Phone_Num', db.String(20), nullable=False)
    allergies = db.Column('Allergies', db.String(255))

    def __init__(self, patient_id, name, date_of_birth, gender, phone, allergies):
        self.patient_id = patient_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.allergies = allergies

    def json(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "phone": self.phone,
            "allergies": self.allergies
        }
    
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

class Prescription(db.Model):
    __tablename__ = 'prescription'
    appt_datetime = db.Column('Appt_DateTime', db.DateTime, db.ForeignKey('appointment_history.Appt_DateTime'), primary_key=True)
    patient_id = db.Column('Patient_ID', db.Integer, db.ForeignKey('appointment_history.Patient_ID'), nullable=False, primary_key=True)
    prescription_id = db.Column('Prescription_ID', db.Integer, nullable=False, primary_key=True)

    appt = db.relationship('Appointment', primaryjoin = 'Prescription.appt_datetime == Appointment.appt_datetime', backref = 'prescription')
    appt1 = db.relationship('Appointment', primaryjoin = 'Prescription.patient_id == Appointment.patient_id', backref = 'prescription')

    def __init__(self, appt_datetime, patient_id, prescription_id):
        self.appt_datetime = appt_datetime
        self.patient_id = patient_id
        self.prescription_id = prescription_id
        
    def json(self):
        return {
            "appt_datetime": self.appt_datetime,
            "patient_id": self.patient_id,
            "prescription_id": self.prescription_id
        }

class PrescriptionMedicine(db.Model):
    __tablename__ = 'prescription_medicines'
    prescription_id = db.Column('Prescription_ID', db.Integer, db.ForeignKey('prescription.Prescription_ID'), primary_key=True)
    medicine_name = db.Column('Medicine_Name', db.String(255), nullable=False, primary_key=True)
    frequency = db.Column('Frequency', db.String(255), nullable=False)
    amount = db.Column('Amount', db.String(255), nullable=False)
    
    prescription = db.relationship('Prescription', primaryjoin = 'PrescriptionMedicine.prescription_id == Prescription.prescription_id', backref = 'prescription_medicines')

    def __init__(self, prescription_id, medicine_name, frequency, amount):
        self.prescription_id = prescription_id
        self.medicine_name = medicine_name
        self.frequency = frequency
        self.amount = amount

    def json(self):
        return {"prescription_id": self.prescription_id, 
                "medicine_name": self.medicine_name,
                "frequency": self.frequency,
                "amount": self.amount
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
    app.run(port=5201, debug=True)

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