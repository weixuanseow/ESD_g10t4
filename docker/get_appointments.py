# Import Flask’s version of SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Query available booking slot from current time 
from datetime import datetime, timedelta
import requests

app = Flask(__name__)
# specify the database URL. Here we use the mysql+mysqlconnector prefix to tell SQLAlchemy which database engine and connector we are using. 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/bookings'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#  disable modification tracking
db = SQLAlchemy(app)
CORS(app)

import mysql.connector
# Configure MySQL connection
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'patient_records',
    'port': 3306
}
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'patient_records',
#     'port': 3306
# }
conn = mysql.connector.connect(**mysql_config)

class AppointmentHistory(db.Model):
    __tablename__ = 'appointment_history'


    appt_datetime = db.Column(db.DateTime, primary_key=True)
    patient_id = db.Column(db.Integer, primary_key=True, nullable=False)
    diagnosis = db.Column(db.String(255), nullable=True)

    def __init__(self, appt_datetime, patient_id, diagnosis):
        self.appt_datetime = appt_datetime
        self.patient_id = patient_id
        self.diagnosis = diagnosis


    def json(self):
        return {"appt_datetime": self.appt_datetime, "patient_id": self.patient_id, "diagnosis": self.diagnosis}
    
    
@app.route("/find_by_date2/<string:date>", methods=["GET"])
def findByDate(date):
    # return date
    appointment_list = AppointmentHistory.query.all()
    if len(appointment_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
                    "bookings": [appointment.json() for appointment in appointment_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no booking slot."
        }
    ), 404
    
    
@app.route('/find_by_date/<int:patient_id>/<string:date>/<string:diagnosis>', methods=['GET'])
def update_patient(patient_id,date,diagnosis):
    date_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    appointment = AppointmentHistory.query.filter_by(appt_datetime=date_time,patient_id=patient_id).first()
    if appointment:
        # data = request.get_json()
        # if data['diagnosis']:
        #     appointment.diagnosis= data['diagnosis']
        appointment.diagnosis=diagnosis
        db.session.commit()
        
        return jsonify(
            {
                "code": 200,
                "data": appointment.json()
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "data": {
                "patient_id": patient_id
            },
            "message": "appointment not found."
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

if __name__ == '__main__':
    app.run(port=5010, debug=True)
    
