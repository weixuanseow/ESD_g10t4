from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#db_name = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/${db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cursor = db.cursor()

# Models


#############################################
# in our scenario 1, the appt microservice must find available time slots for different types
# of test like x-ray, mri, ct scan, etc then update accordingly

# maybe need another db?

############################################
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

class DiagnosticTest(db.Model):
    __tablename__ = 'diagnostic_test'
    test_id = db.Column('Test_ID', db.Integer, primary_key=True, autoincrement=True)
    test_datetime = db.Column('Test_DateTime', db.DateTime, nullable=False)
    test_type = db.Column('Test_Type', db.String(255), nullable=False)
    test_results = db.Column('Test_Results', db.String(255), nullable=False)
    patient_id = db.Column('Patient_ID', db.Integer, db.ForeignKey('appointment_history.Patient_ID'), nullable=False)
    appt_datetime = db.Column('Appt_DateTime', db.DateTime, db.ForeignKey('appointment_history.Appt_DateTime'), nullable=False)

    def __init__(self, test_id, test_datetime, test_type, test_results, patient_id, appt_datetime):
        self.test_id = test_id
        self.test_datetime = test_datetime
        self.test_type = test_type
        self.test_results = test_results
        self.patient_id = patient_id
        self.appt_datetime = appt_datetime

    def json(self):
        return {"test_id": self.test_id,
                "test_datetime": self.test_datetime,
                "test_type": self.test_type,
                "test_results": self.test_results,
                "patient_id": self.patient_id,
                "appt_datetime": self.appt_datetime
        }
        
    appt = db.relationship('Appointment', primaryjoin = 'DiagnosticTest.patient_id == Appointment.patient_id', backref = 'diagnostic_test')
    appt = db.relationship('Appointment', primaryjoin = 'DiagnosticTest.appt_datetime == Appointment.appt_datetime', backref = 'diagnostic_test')
    

# Routes
# find available time slots

# add diagnostic test










if __name__ == '__main__':
    app.run(port=5000, debug=True)
