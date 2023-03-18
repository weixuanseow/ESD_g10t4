from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Query available booking slot from current time 
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/diagnostic_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)

import mysql.connector
# Configure MySQL connection
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'diagnostic_test',
    'port': 3306
}
conn = mysql.connector.connect(**mysql_config)

class xray(db.Model):
    __tablename__ = 'xray'

    bid = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    pid = db.Column(db.String(255))

    def __init__(self, bid, slot, available, pid):
        self.bid = bid
        self.slot = slot
        self.available = available
        self.pid = pid


    def json(self):
        return {"bid": self.bid, "slot": self.slot, "available": self.available, 'pid':self.pid}

class DiagnosticTest(db.Model):
    __tablename__ = 'test'
    
    test_id = db.Column(db.Integer, primary_key=True)
    test_datetime = db.Column(db.DateTime, nullable=False)
    test_type = db.Column(db.String, nullable=False)
    test_results = db.Column(db.String, nullable=False)
    
    def __init__(self, test_id, test_datetime, test_type, test_results):
        self.test_id = test_id
        self.test_datetime = test_datetime
        self.test_type = test_type
        self.test_results = test_results
        
    def json(self):
        return {"tid": self.test_id, "date_time": self.test_datetime, "test_type": self.test_type, "result": self.test_results}
    
#################### DIAGNOSTIC TEST RELATED FUNCTIONS ############################################################
# create diagnostic test for scenario 1
@app.route('/create_diagnostic_test/xray/', methods=['POST'])
def createDiagnosticTest():
    data = request.get_json()
    test_instance = DiagnosticTest(**data)
    try:
        db.session.add(test_instance)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "test_id": "error message in the except portion"
                },
                "message": "An error occured creating the test instance"
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": test_instance.json()
        }
    ), 201

# just to view diagnostic_test database, 'test' table
@app.route('/view_diagnostic_test/', methods=['GET'])
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
            "message": "There are no booking slot."
        }
    ), 404
    
    
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)

