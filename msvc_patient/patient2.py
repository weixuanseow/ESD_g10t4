from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__ = 'patient'
    
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_full_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    allergies = db.Column(db.String(255))

    def __init__(self, patient_id, patient_full_name, date_of_birth, gender, phone_num, allergies):
        self.patient_id = patient_id
        self.patient_full_name = patient_full_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_num = phone_num
        self.allergies = allergies
        
    def json(self):
        return {
            "patient_id": self.patient_id,
            "name": self.patient_full_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "phone": self.phone_num,
            "allergies": self.allergies
        }
    
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
            "message": "There are no booking slot."
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
@app.route('/patients', methods=['POST'])
def create_patient():
    
    data = request.get_json()
    name = data['Patient_Full_Name']
    date_of_birth = data['Date_Of_Birth']
    gender = data['Gender']
    phone_num = data['Phone_Num']
    allergies = data['Allergies']
    
    # Check if patient already exists
    if Patient.query.filter_by(name=name, date_of_birth=date_of_birth, gender=gender, phone_num=phone_num).first():
        return jsonify(
            {
                "code": 400,
                "message": "Patient already exists!"
            }
        ), 400
    
    # If patient doesn't exist, insert patient into database
    new_patient = Patient(name=name, date_of_birth=date_of_birth, gender=gender, phone_num=phone_num, allergies=allergies)
    try:
        db.session.add(new_patient)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "name": name,
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
    patient = Patient.query.filter_by(patient_ID=patient_id).first()
    if patient:
        data = request.get_json()
        if data['Patient_Full_Name']:
            patient.Patient_Full_Name = data['Patient_Full_Name']
        if data['Date_Of_Birth']:
            patient.Date_Of_Birth = data['Date_Of_Birth']
        if data['Gender']:
            patient.Gender = data['Gender']
        if data['Phone_Num']:
            patient.Phone_Num = data['Phone_Num'] 
        if data['Allergies']:
            patient.Allergies = data['Allergies'] 
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

# create diagnostic test for scenario 1


if __name__ == '__main__':
    app.run(port=5000, debug=True)
