from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 

import requests

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# cursor = db.cursor()

#dispense_restock_URL = "http://localhost:5202"
# dispense_restock_url = "http://localhost:5200/update_inventory"
##actually now i am worried if this is in the right place shd this be in the UI instead or sth

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
#Update stock level/s + Return success/failure message and associated amount/s that must be topped up
# @app.route('/update_inventory', methods=['PUT']) ##MINNAL: Route and input variable could be modified to be better
# def update_inventory():
#     data = request.get_json()
#     print (data)
#     ret_list=[]
#     if data is not None:
#         try:
#             for drug_name, qty in data.items():
#                 drug_full_name = Inventory.query.filter(Inventory.drug_full_name == drug_name).first()
#                 print(drug_name)
#                 print(qty)
#                 drug_full_name.current_amt -= qty
#                 db.session.commit()

#                 if drug_full_name.current_amt <= drug_full_name.threshold_amt:
#                     ret_list.append((drug_full_name.drug_full_name, drug_full_name.topup_amt))

#             if len(ret_list)>0:
#                 return jsonify(
#                     {
#                         "code": 200,
#                         "data": ret_list, 
#                         "message": 'Inventory has been updated successfully. Quantity of some medicines needs to be topped up.'
#                     }
#                 )
#             else:
#                 return jsonify(
#                     {
#                     "code": 210,
#                     "message": 'Inventory has been updated successfully.'
#                     }
#                 )
#         except:
#             return jsonify(
#                 {
#                 "code": 500,
#                 "message": 'An error occurred while updating the inventory.'
#                 }
#             )
    
#     return jsonify(
#         {
#         "code": 404,
#         "message": 'No data was received. Inventory was not updated.'
#         }
#     )


@app.route('/update_inventory', methods=['PUT'])
def update_inventory():
    data = request.get_json()
    
    updated = False  # flag to indicate whether any updates were made
    
    try:
        ret_list={}
        for drug_name, qty in data.items():
            drug_full_name = Inventory.query.filter(Inventory.drug_full_name == drug_name).first()
            drug_full_name.current_amt -= qty
            if drug_full_name.current_amt<=drug_full_name.threshold_amt:
                ret_list[drug_full_name.drug_full_name]=drug_full_name.topup_amt
            updated = True  # set the flag to True if an update was made
            db.session.commit()
        
        if updated:
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
     app.run(port=5200, debug=True)
