#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import sys
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

db = SQLAlchemy(app)
cursor = db.cursor()

patient_URL = "http://localhost:5004/patient/<int:patient_id>"

# @app.route("/pharmacy/<str:patient_id>/<string:appt_datetime>", methods=['GET'])
# def find_by_appt(appt_datetime):
#     patient = invoke_http(patient_URL, method='GET', json=patient)
#     appt = patient['']
#     prescription_details = 
#     if book:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": book.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "No prescription found."
#         }
#     ), 404

@app.route('/<string:appt_datetime>', methods=['POST'])
def receive_info():
    info = request.get_json()
    # process the info as needed
    return f'Received info: {info}'


if __name__ == '__main__':
    app.run(port=5201, debug=True)