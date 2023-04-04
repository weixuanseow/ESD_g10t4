import requests
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)
# Models
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
        dto = {
            "appt_datetime": self.appt_datetime,
            "patient_id": self.patient_id,
            "prescription_id": self.prescription_id
        }
        
        dto['medication'] = []
        for med in self.medication:
            dto['medication'].append(med.json())
        return dto

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
    
# Route
PATIENT_MICROSERVICE_URL = environ.get('patientURL') or "http://127.0.0.1:5051/"
DRUG_MICROSERVICE_URL = environ.get('drugURL') or "http://127.0.0.1:5002/"

#creates prescription record 
@app.route('/prescribe_medicine', methods=["POST"])
def prescribe_medicine(): 
    data = request.get_json()
    patient_id = data['patient_id']
    prescription_details = data['prescription_details']
    appt_date = data['appt_date']
    print(prescription_details)
    
    # invoke patient microservice
    print('\n-----Invoking patient microservice-----')    
    allergies = invoke_http(f"{PATIENT_MICROSERVICE_URL}patient/{patient_id}/allergies", method='GET')
    print('allergies:', allergies)
        
    medicine_names = [med['med_name'] for med in prescription_details]
    drug_service_payload = {
        'patient_id': patient_id,
        'medicine_names': medicine_names,
        'allergies': allergies
    }
    # invoke drug microservice
    response = invoke_http(f"{DRUG_MICROSERVICE_URL}check-interaction", method='GET', json=drug_service_payload)
    error_code = response['code']
    
    if error_code == 400:
        # patient is allergic to a medicine or there are harmful interactions
        # send message to UI to prompt doctor to re-enter medicine details
        error_message = response['message']
        return jsonify(
            {
                'code': error_code,
                'message': error_message
            }
        )
    elif error_code == 422:
        error_message = response['message']
        return jsonify({
            'code': error_code,
            'message': error_message
        })
    else:
        # no harmful interactions, update prescription history in patient microservice
        prescription_payload = {
            'patient_id': patient_id,
            # appt_datetime from homepage , hardcoded for now for patient 3
            # 'appt_datetime': '2023-03-11 16:30:00',
            'appt_datetime': appt_date
        }
        response = requests.put(f"{PATIENT_MICROSERVICE_URL}update-prescription-history", json=prescription_payload)
        prescription_id = response.json()['prescription_id']
        
        # update prescription_medicines table in patient microservice
        prescription_medicines_payload = {
            'prescription_id': prescription_id,
            'medicine_details': prescription_details
        }
        response = requests.put(f"{PATIENT_MICROSERVICE_URL}update-prescription-medicines", json=prescription_medicines_payload)
        
        return jsonify(
            {
                'code': 200,
                'message': 'Prescription successfully added to patient history'
            }
        )
    

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for prescribing medicine...")
    app.run(host="0.0.0.0", port=5101, debug=True)