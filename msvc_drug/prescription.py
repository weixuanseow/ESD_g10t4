from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cursor = db.cursor()

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
    
    
# Routes


############ compare drugs & allergy








# find patient & allergy

# @app.route('/patient/<int:patient_id>', methods=['GET'])
# def find_patient(patient_id):
    # patient = Patient.query.filter_by(patient_id=patient_id).first()
    # if patient:
    #     return jsonify(
    #         {
    #             "code": 200,
    #             "data": patient.json()
    #         }
    #     )
    # return jsonify(
    #     {
    #         "code": 404,
    #         "message": "Patient not found."
    #     }
    # ), 404




# create patient prescription######################

# @app.route('/patients', methods=['POST'])
# def create_patient():
    
#     data = request.get_json()
#     name = data['Patient_Full_Name']
#     date_of_birth = data['Date_Of_Birth']
#     gender = data['Gender']
#     phone_num = data['Phone_Num']
#     allergies = data['Allergies']
    
#     # Check if patient already exists
#     if Patient.query.filter_by(name=name, date_of_birth=date_of_birth, gender=gender, phone_num=phone_num).first():
#         return jsonify(
#             {
#                 "code": 400,
#                 "message": "Patient already exists!"
#             }
#         ), 400
    
#     # If patient doesn't exist, insert patient into database
#     new_patient = Patient(name=name, date_of_birth=date_of_birth, gender=gender, phone_num=phone_num, allergies=allergies)
#     try:
#         db.session.add(new_patient)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "name": name,
#                     "date_of_birth": date_of_birth,
#                     "gender": gender,
#                     "phone_num": phone_num,
#                     "allergies": allergies
#                 },
#                 "message": "An error occurred creating the Patient record."
#             }
#         ), 500
        
#     return jsonify(
#         {
#             "code": 201,
#             "data": new_patient.json(),
#             "message": "Patient created successfully"
#         }
#     ), 201    
        
        
        
        ####################################################################
# update patient prescription
# @app.route('/patients/<int:patient_id>', methods=['PUT'])
# def update_patient(patient_id):
#     patient = Patient.query.filter_by(patient_ID=patient_id).first()
#     if patient:
#         data = request.get_json()
#         if data['Patient_Full_Name']:
#             patient.Patient_Full_Name = data['Patient_Full_Name']
#         if data['Date_Of_Birth']:
#             patient.Date_Of_Birth = data['Date_Of_Birth']
#         if data['Gender']:
#             patient.Gender = data['Gender']
#         if data['Phone_Num']:
#             patient.Phone_Num = data['Phone_Num'] 
#         if data['Allergies']:
#             patient.Allergies = data['Allergies'] 
#         db.session.commit()
        
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": patient.json()
#             }
#         )
        
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "patient_id": patient_id
#             },
#             "message": "Patient not found."
#         }
#     ), 404
    
    
    
    # if not patient:
    #     return {"error": "Patient not found"}, 404

    # data = request.get_json()
    # patient.Patient_Full_Name = data.get('Patient_Full_Name', patient.Patient_Full_Name)
    # patient.Date_Of_Birth = data.get('Date_Of_Birth', patient.Date_Of_Birth)
    # patient.Gender = data.get('Gender', patient.Gender)
    # patient.Phone_Num = data.get('Phone_Num', patient.Phone_Num)
    # patient.Allergies = data.get('Allergies', patient.Allergies)

    # db.session.commit()
    # return {"message": "Patient record updated successfully"}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
