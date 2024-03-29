from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from os import environ

import logging
import json
import traceback

# Query available booking slot from current time 
from datetime import datetime, timedelta

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/patient_records'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:@localhost:3306/patient_records'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)
CORS(app)

# import mysql.connector
# Configure MySQL connection
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'root',
#     'database': 'patient_records',
#     'port': 8889
# }

# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'patient_records',
#     'port': 3306
# }
# conn = mysql.connector.connect(**mysql_config)
        
class ApptHist(db.Model):
    __tablename__ = 'appointment_history'
    
    patient_id = db.Column(db.ForeignKey(
        'patient_records.patient', ondelete='CASCADE', onupdate='CASCADE'), 
                           nullable=False, primary_key = True)
    appt_datetime = db.Column(db.DateTime, primary_key=True)
    diagnosis = db.Column(db.String(255), nullable=False)
    
    def __init__(self, appt_datetime, diagnosis):
        # self.patient_id = patient_id
        self.appt_datetime = appt_datetime
        self.diagnosis = diagnosis
    
    def json(self):
        return {
            'patient_id': self.patient_id,
            'appt_datetime': self.appt_datetime,
            'diagnosis': self.diagnosis
        }
    
class Patient(db.Model):
    __tablename__ = 'patient'
    
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_full_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    # gender = db.Column(db.String(3), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    allergies = db.Column(db.String(64))
    
    def __init__(self, patient_full_name, date_of_birth, gender, phone_num, allergies):
        # self.patient_id = patient_id
        self.patient_full_name = patient_full_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_num = phone_num
        self.allergies = allergies
    
    def json(self):
        return {
            'patient_id': self.patient_id,
            'patient_fullname': self.patient_full_name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'phone_num': self.phone_num,
            'allergies': self.allergies
        }
        
class PrescriptionMedicine(db.Model):
    __tablename__ = 'prescription_medicines'
    
    prescription_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(100))
    frequency = db.Column(db.String(255))
    amount = db.Column(db.String(255))
    
    def __init__(self, prescription_id, medicine_name, frequency, amount):
        # self.patient_id = patient_id
        self.prescription_id = prescription_id
        self.medicine_name = medicine_name
        self.frequency = frequency
        self.amount = amount
    
    def json(self):
        return {
            'prescription_id': self.prescription_id,
            'medicine_name': self.medicine_name,
            'frequency': self.frequency,
            'amount': self.amount
        }
        
# class Prescription(db.Model):
#     __tablename__ = 'prescription'
    
#     appt_datetime = db.Column(db.ForeignKey('patient_records.appointment_history', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
#     patient_id = db.Column(db.ForeignKey('patient_records.appointment_history', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
#     prescription_id = db.Column(db.ForeignKey('patient_records.prescription_medicines', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    
#     def __init__(self, appt_datetime, patient_id):
#         self.appt_datetime = appt_datetime
#         self.patient_id = patient_id
#         # self.prescription_id = prescription_id
    
#     def json(self):
#         return {
#             'prescription_id': self.prescription_id,
#             'patient_id': self.patient_id,
#             'appt_datetime': self.appt_datetime
#         }
        
class Prescription(db.Model):
    __tablename__ = 'prescription'
    
    appt_datetime = db.Column(db.ForeignKey('appointment_history.appt_datetime', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    patient_id = db.Column(db.ForeignKey('appointment_history.patient_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    def __init__(self, appt_datetime, patient_id):
        self.appt_datetime = appt_datetime
        self.patient_id = patient_id
    
    def json(self):
        return {
            'prescription_id': self.prescription_id,
            'patient_id': self.patient_id,
            'appt_datetime': self.appt_datetime
        }

class DiagnosticTest(db.Model):
    __tablename__ = 'diagnostic_test'
    
    test_id = db.Column(db.Integer, primary_key=True)
    test_datetime = db.Column(db.DateTime, nullable=False)
    test_type = db.Column(db.String, nullable=False)
    test_results = db.Column(db.String, nullable=False)
     
    # Foreign keys point to APPOINTMENT HISTORY table
    patient_id = db.Column(db.ForeignKey('appointment_history.patient_id'), nullable=False)
    appt_datetime = db.Column(db.ForeignKey('appointment_history.appt_datetime'), nullable=False)
    
    def __init__(self, patient_id, test_datetime, test_type, test_results, appt_datetime):
        self.patient_id = patient_id
        self.test_datetime = test_datetime
        self.test_type = test_type
        self.test_results = test_results
        self.appt_datetime = appt_datetime
   
        
    def json(self):
        return {"test_id": self.test_id, 
                "test_datetime": self.test_datetime, 
                "test_type": self.test_type, 
                "test_results": self.test_results,
                "patient_id": self.patient_id,
                "appt_datetime": self.appt_datetime
                }

##############  PATIENT RELATED FUNCTIONS   ##############################################
@app.route("/patient", methods=['GET'])
def get_all():
    patient_list = Patient.query.all()
    if len(patient_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [patient.json() for patient in patient_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no patients."
        }
    ), 404

# find patient
@app.route('/patient/<int:patient_id>', methods=['GET'])
def find_patient(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        return jsonify(
            {
                "code": 200,
                "data": patient.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Patient not found."
        }
    ), 404

# create patient
@app.route('/patients/create', methods=['POST'])
def create_patient():
    
    data = request.get_json()
    
    patient_full_name = data['patient_full_name']
    date_of_birth = data['date_of_birth']
    gender = data['gender']
    phone_num = data['phone_num']
    allergies = data['allergies']
    
    # Check if patient already exists
    if Patient.query.filter_by(patient_full_name=patient_full_name, date_of_birth=date_of_birth, gender=gender, phone_num=phone_num).first():
        return jsonify(
            {
                "code": 400,
                "message": "Patient already exists!"
            }
        ), 400
    
    # If patient doesn't exist, insert patient into database
    new_patient = Patient(patient_full_name=patient_full_name, date_of_birth=date_of_birth, gender=gender, phone_num=phone_num, allergies=allergies)
    try:
        db.session.add(new_patient)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "patient_full_name": patient_full_name,
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "phone_num": phone_num,
                    "allergies": allergies
                },
                "message": "An error occurred creating the Patient record."
            }
        ), 500
        
    return jsonify(
        {
            "code": 201,
            "data": new_patient.json(),
            "message": "Patient created successfully"
        }
    ), 201    
        
# update patient
@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        data = request.get_json()
        if data['patient_full_name']:
            patient.patient_full_name = data['patient_full_name']
        if data['date_of_birth']:
            patient.date_of_birth = data['date_of_birth']
        if data['gender']:
            patient.gender = data['gender']
        if data['phone_num']:
            patient.phone_num = data['phone_num'] 
        if data['allergies']:
            patient.allergies = data['allergies'] 
        db.session.commit()
        
        return jsonify(
            {
                "code": 200,
                "data": patient.json()
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "data": {
                "patient_id": patient_id
            },
            "message": "Patient not found."
        }
    ), 404
    
    
    
    if not patient:
        return {"error": "Patient not found"}, 404

    data = request.get_json()
    patient.Patient_Full_Name = data.get('Patient_Full_Name', patient.Patient_Full_Name)
    patient.Date_Of_Birth = data.get('Date_Of_Birth', patient.Date_Of_Birth)
    patient.Gender = data.get('Gender', patient.Gender)
    patient.Phone_Num = data.get('Phone_Num', patient.Phone_Num)
    patient.Allergies = data.get('Allergies', patient.Allergies)

    db.session.commit()
    return {"message": "Patient record updated successfully"}, 200

    
@app.route('/patient/<int:patient_id>/allergies', methods=["GET"])
def get_patient_allergies(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    if patient:
        allergies = patient.allergies or ''
        return jsonify(allergies.split(','))
    return jsonify(
        {
            "code": 404,
            "message": "Patient not found."
        }
    ), 404



###################################################################################################################
#################### DIAGNOSTIC TEST RELATED FUNCTIONS ############################################################
@app.route('/create_diagnostic_test', methods=['POST'])
def createDiagnosticTest():
    try:
        data = request.get_json()
        print(data)
        # pid = data['pid']
        pid = data['pid']
        from datetime import datetime
        now = datetime.now()
        test_datetime = now.strptime(data['bslot'], ' %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')
        test_type = data["test_type"]
        test_results = "Broken brain cells"
        appt_datetime = data['appt']
        
         # check if patient ID exists
        if not Patient.query.filter_by(patient_id=pid).first():
            return jsonify({'error': 'Patient does not exist.'}), 400

        # check if diagnostic test exists for patient
        if DiagnosticTest.query.filter_by(patient_id=pid, appt_datetime=appt_datetime).first():
            return jsonify({'error': 'Diagnostic test already exists for the patient.'}), 400

        # create new DiagnosticTest object
        test = DiagnosticTest(patient_id=pid, test_datetime=test_datetime, test_type=test_type, test_results=test_results,
                    appt_datetime=appt_datetime)


        # Add the test to the database
        db.session.add(test)
        db.session.commit()

        return jsonify({
            'code': 201,
            'message': 'Diagnostic test created successfully.'
            })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify(
            {
                "code": 500,
                "message": f"An error occurred creating the test: {str(e)}"
            }
        ), 500

# just to view diagnostic_test database, 'test' table
@app.route('/view_diagnostic_test', methods=['GET'])
def viewDiagnosticTest():
    test_list = DiagnosticTest.query.all()
    if len(test_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [test.json() for test in test_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no diagnostic test slot."
        }
    ), 404
    
################################################################################################################
#################### PRESCRIPTION RELATED FUNCTIONS ############################################################
@app.route('/check_prescription/<patient_id>/<appt_date>', methods=['GET']) #wehhh i havent figured out the input stuff yet
def check_prescription(patient_id, appt_date):
    print(patient_id,appt_date)
    print(type(patient_id),type(appt_date))
    #appt_date='2022-12-28' #need to remove this hardcode aft adding more data in!
    prescription = Prescription.query.filter(Prescription.patient_id == patient_id,func.DATE(Prescription.appt_datetime) == appt_date).first()
   
    if prescription:
        prescription_medicines = PrescriptionMedicine.query.filter_by(prescription_id=prescription.prescription_id).all()
        if prescription_medicines:
            medicines = {}
            for medicine in prescription_medicines:
                medicines[medicine.medicine_name]= medicine.amount
                    # "medicine_name": medicine.medicine_name,
                    # "amount": medicine.amount #is amt right not freq*amt
                
            return jsonify(
                {
                    "code": 250, #random number can change
                    "data": medicines,
                    "message": "Prescription created for this patient on this appointment date has been found."
                }
            ), 250
    print('code 404')
    return jsonify(
        {
            "code": 404,
            "message": "There was no prescription found for this patient on this appointment date."
        }
    ), 404

@app.route('/update-prescription-history', methods=['PUT'])
def update_prescription_history():
    data = request.get_json()
    # appt_datetime need to retrieve from homepage, hardcode first
    appt_datetime = data['appt_datetime']
    patient_id = data['patient_id']
    
    prescription = Prescription(appt_datetime=appt_datetime, patient_id=patient_id)
    db.session.add(prescription)
    db.session.commit()
    
    # get prescription ID
    prescription_id = prescription.prescription_id
    return jsonify({'prescription_id': prescription_id})


@app.route('/update-prescription-medicines', methods=['PUT'])
def update_prescription_medicines():
    data = request.get_json()
    prescription_id = data['prescription_id']
    medicines = data['medicine_details']
    print(medicines)
    prescription_medicines = []

    for med in medicines:
        medicine_name = med['med_name']
        frequency = med['frequency']
        amount = med['amount']
        prescription_medicine = PrescriptionMedicine(prescription_id=prescription_id, medicine_name=medicine_name, frequency=frequency, amount=amount)
        prescription_medicines.append(prescription_medicine)

    db.session.add_all(prescription_medicines)
    db.session.commit()

    return jsonify({'message': 'Prescription medicines updated successfully'})
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051, debug=True)

