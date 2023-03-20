from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient_records'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cursor = db.cursor()

dispense_restock_URL = "http://localhost:5202"

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
#Update stock level/s + Return updated stock level/s

#receive list of [(name, amt to reduce by)] frm complex microservice
#find drug_full_name=name, update db with current_amt-=amt to reduce by
#update db
#check if current_amt<=threshold_amt -- i made it <= cos i think == threshold shd be concerning enough alr
#if yes: return (db updated success msg, [(drug_full_name, topup_amt)]
#if no: return (db updated success msg, [])

##complex microservice shd read the success msg and read the list to see if anth needs to be topped up!

@app.route('/ROUTE/<INPUT>', methods=['PUT']) ### NEED TO FIX
def update_inventory(INPUT):
    data = request.get_json()
    ret_list=[]
    if data:
        for i in data: ###can json be a list???
            drug_name = i[0]
            qty = i[1]
            drug_full_name = Inventory.query.filter_by(drug_full_name=drug_name).first()
            drug_full_name.current_amt -= qty
            if drug_full_name.current_amt<=drug_full_name.threshold_amt:
                ret_list.append((drug_full_name.drug_full_name, drug_full_name.topup_amt))

        db.session.commit()

        #return ['inventory has been updated successfully', ret_list]
        if len(ret_list)>0:
            return jsonify(
                {
                    "code": 200,
                    "data": ret_list.json(), 
                    "message": 'Inventory has been updated successfully. Quantity of some medicines needs to be topped up.'
                }
            )
        else:
            return jsonify(
                {
                "code": 200,
                "message": 'Inventory has been updated successfully.'
                }
            )
    
    #return ['error, no data was received and inventory was not updated']
    return jsonify(
        {
        "code": 404,
        "message": 'No data was received. Inventory was not updated.'
        }
    )

# need to have one that sends 
requests.post(url, data=None, json=None, **kwargs)


if __name__ == '__main__':
     app.run(port=5200, debug=True)
