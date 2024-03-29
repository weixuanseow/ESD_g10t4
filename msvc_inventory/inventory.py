from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from os import environ

import requests

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Inventory(db.Model):
    __tablename__ = 'inventory'
    drug_full_name = db.Column('Drug_Full_Name', db.String(64), nullable=False, primary_key=True)
    current_amt = db.Column('Current_Amt', db.Integer, nullable=False)
    threshold_amt = db.Column('Threshold_Amt', db.Integer, nullable=False)
    topup_amt = db.Column('Topup_Amt', db.Integer, nullable=False)

    def __init__(self, drug_full_name, current_amt, threshold_amt, topup_amt):
        self.drug_full_name = drug_full_name
        self.current_amt = current_amt
        self.threshold_amt = threshold_amt
        self.topup_amt = topup_amt

    def json(self):
        return {"drug_full_name": self.drug_full_name,
                "current_amt": self.current_amt,
                "threshold_amt": self.threshold_amt,
                "topup_amt": self.topup_amt
        }
    

# Routes
# updates inventory when drug has been dispensed and also checks if any drug needs to be restocked
@app.route('/update_inventory', methods=['PUT'])
def update_inventory():
    data = request.get_json()
    print(data)
    
    updated = False  # flag to indicate whether any updates were made
    
    try:
        print('checkpoint1')
        ret_list={}
        print('checkpoint2')
        for drug_name, qty in data.items():
            print('checkpoint3')
            drug_full_name = Inventory.query.filter(Inventory.drug_full_name == drug_name).first()
            drug_full_name.current_amt -= qty
            print('checkpoint4')
            if drug_full_name.current_amt<=drug_full_name.threshold_amt:
                print('checkpoint5')
                ret_list[drug_full_name.drug_full_name]=drug_full_name.topup_amt
            updated = True  # set the flag to True if an update was made
            print('checkpoint6')
            db.session.commit()
            print('checkpoint7')
        if updated:
            print('checkpoint8')
            return jsonify(
                {
                    "code": 200,
                    "data": ret_list,  # return all updated drugs
                    "message": 'Updates were made and topups are required.'
                }
            ), 200

        else:
            return jsonify(
                {
                    "code": 210,
                    "message": "No updates were made"
                }
            ), 210
    
    #Return any errors faced 
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the inventory. " + str(e)
            }
        ), 500


if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5211, debug=True)