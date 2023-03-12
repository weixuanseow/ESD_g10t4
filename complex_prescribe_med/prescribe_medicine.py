from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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