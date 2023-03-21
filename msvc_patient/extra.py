# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

# # Query available booking slot from current time 
# from datetime import datetime, timedelta

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# CORS(app)

# import mysql.connector
# # Configure MySQL connection
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'patient_records',
#     'port': 3306
# }
# conn = mysql.connector.connect(**mysql_config)

# # class xray(db.Model):
# #     __tablename__ = 'xray'

# #     bid = db.Column(db.Integer, primary_key=True)
# #     slot = db.Column(db.DateTime, nullable=False)
# #     available = db.Column(db.Boolean, default=True)
# #     pid = db.Column(db.String(255))

# #     def __init__(self, bid, slot, available, pid):
# #         self.bid = bid
# #         self.slot = slot
# #         self.available = available
# #         self.pid = pid


# #     def json(self):
# #         return {"bid": self.bid, "slot": self.slot, "available": self.available, 'pid':self.pid}

# class DiagnosticTest2(db.Model):
#     __tablename__ = 'fkit'
    
#     test_id = db.Column(db.Integer, primary_key=True)
#     test_datetime = db.Column(db.DateTime, nullable=False)
#     test_type = db.Column(db.String, nullable=False)
#     test_results = db.Column(db.String, nullable=False)
    
#     # Foreign keys point to APPOINTMENT HISTORY table
#     patient_id = db.Column(db.Integer, nullable=False)
#     appt_datetime = db.Column(db.DateTime, nullable=False)
    
#     def __init__(self, test_datetime, test_type, test_results, patient_id, appt_datetime):
#         # self.test_id = test_id
#         self.test_datetime = test_datetime
#         self.test_type = test_type
#         self.test_results = test_results
#         self.patient_id = patient_id
#         self.appt_datetime = appt_datetime
        
#     def json(self):
#         return {"tid": self.test_id, 
#                 "test_datetime": self.test_datetime, 
#                 "test_type": self.test_type, 
#                 "test_results": self.test_results,
#                 "patient_id": self.patient_id,
#                 "appt_datetime": self.appt_datetime
#                 }
        
# class ApptHist(db.Model):
#     __tablename__ = 'appointment_history'
    
#     patient_id = db.Column(db.ForeignKey(
#         'patient_records.patient', ondelete='CASCADE', onupdate='CASCADE'), 
#                            nullable=False, primary_key = True)
#     appt_datetime = db.Column(db.DateTime, primary_key=True)
#     diagnosis = db.Column(db.String(255), nullable=False)
    
    
#     def json(self):
#         return {
#             'patient_id': self.patient_id,
#             'appt_datetime': self.appt_datetime,
#             'diagnosis': self.diagnosis
#         }
    
# class Patient(db.Model):
#     __tablename__ = 'patient'
    
#     patient_id = db.Column(db.Integer, primary_key=True)
#     patient_full_name = db.Column(db.String(64), nullable=False)
#     date_of_birth = db.Column(db.DateTime, nullable=False)
#     gender = db.Column(db.String(3), nullable=False)
#     phone_num = db.Column(db.String(20), nullable=False)
#     allergies = db.Column(db.String(64))
    
#     def json(self):
#         return {
#             'patient_id': self.patient_id,
#             'patient_fullname': self.patient_full_name,
#             'date_of_birth': self.date_of_birth,
#             'gender': self.gender,
#             'phone_num': self.phone_num,
#             'allergies': self.allergies
#         }
        
# class PrescriptionMedicine(db.Model):
#     __tablename__ = 'prescription_medicines'
    
#     prescription_id = db.Column(db.Integer, primary_key=True)
#     medicine_name = db.Column(db.String(100))
#     frequency = db.Column(db.String(255))
#     amount = db.Column(db.String(255))
    
#     def json(self):
#         return {
#             'prescription_id': self.prescription_id,
#             'medicine_name': self.medicine_name,
#             'frequency': self.frequency,
#             'amount': self.amount
#         }
        
# class Prescription(db.Model):
#     __tablename__ = 'prescription'
    
#     prescription_id = db.Column(db.ForeignKey('patient_records.prescription_medicines', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
#     patient_id = db.Column(db.ForeignKey('patient_records.appointment_history', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
#     appt_datetime = db.Column(db.ForeignKey('patient_records.appointment_history', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    
#     def json(self):
#         return {
#             'prescription_id': self.prescription_id,
#             'patient_id': self.patient_id,
#             'appt_datetime': self.appt_datetime
#         }
        
# class DiagnosticTest(db.Model):
#     __tablename__ = 'diagnostic_test'
    
#     test_id = db.Column(db.Integer, primary_key=True)
#     test_datetime = db.Column(db.DateTime, nullable=False)
#     test_type = db.Column(db.String, nullable=False)
#     test_results = db.Column(db.String, nullable=False)
    
#     # Foreign keys point to APPOINTMENT HISTORY table
#     patient_id = db.Column(db.ForeignKey('appointment_history.patient_id'), nullable=False)
#     appt_datetime = db.Column(db.ForeignKey('appointment_history.appt_datetime'), nullable=False)
        
#     def json(self):
#         return {"test_id": self.test_id, 
#                 "test_datetime": self.test_datetime, 
#                 "test_type": self.test_type, 
#                 "test_results": self.test_results,
#                 "patient_id": self.patient_id,
#                 "appt_datetime": self.appt_datetime
#                 }
    
    
    
    
    
# #################### DIAGNOSTIC TEST RELATED FUNCTIONS ############################################################
# # create diagnostic test for scenario 1
# @app.route('/create_diagnostic_test/xray', methods=['POST'])
# def createDiagnosticTest():
#     data = request.get_json()
#     print(data)
#     # pid = data['pid']
    
#     test_datetime = data['test_datetime']
#     test_type = data["visit_type"]
#     test_results = data['test_results']
#     patient_id = data["patient_id"]
#     appt_datetime = data["appt_datetime"]
    
#     test_instance = DiagnosticTest2(test_datetime=test_datetime, test_type=test_type, test_results=test_results, patient_id=patient_id, appt_datetime=appt_datetime)
#     print(db.session)
#     # test_type=visit_type
#     try:
#         db.session.add(test_instance)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "test_id": "error message in the except portion",
#                     "test_datetime": test_datetime,
#                     "test_type": test_type,
#                     "test_results": test_results,
#                 },
#                 "message": "An error occured creating the test instance"
#             }
#         ), 500
#     return jsonify(
#         {
#             "code": 201,
#             "data": test_instance.json(),
#             "message": "Donezo mina san"
#         }
#     ), 201


# @app.route('/create_diagnostic_test', methods=['POST'])
# def createDiagnosticTest2():
#     if request.method == "POST":
#         data = request.get_json()
#         print("IF BLOCK ENTERED")
#         test_datetime = data['test_datetime']
#         test_type = data["visit_type"]
#         test_results = data['test_results']
#         patient_id = data["patient_id"]
#         appt_datetime = data["appt_datetime"]
        
#         cur = mysql.cursor()
#         cur.execute(f"INSERT INTO diagnostic_test (test_datetime, test_type, test_results, patient_id, appt_datetime) VALUES ({test_datetime}, {test_type}, {test_results}, {patient_id}, {appt_datetime})")
#         mysql.connection.commit()
        
#     return {
#         "YOLO": "yolo"
#     }


# # just to view diagnostic_test database, 'test' table
# @app.route('/view_diagnostic_test', methods=['GET'])
# def viewDiagnosticTest():
#     test_list = DiagnosticTest.query.all()
#     if len(test_list):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     # we use for book to perform an iteration and create a JSON representation of it using book.json() function.
#                     "bookings": [test.json() for test in test_list]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no booking slot."
#         }
#     ), 404
    
    
    
# if __name__ == '__main__':
#     app.run(port=5050, debug=True)

