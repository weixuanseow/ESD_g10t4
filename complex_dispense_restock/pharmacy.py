#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/pharmacy", methods=['POST'])
def receiveLog():
    # Check if the request contains valid JSON
    log = None
    if request.is_json:
        log = request.get_json()
        processLog(log)
        # reply to the HTTP request
        return jsonify({"code": 200, "data": 'OK. Drug dispensed successfully.'}), 200 # return message; can be customized
    else:
        log = request.get_data()
        print("Received an invalid log:")
        print(log)
        print()
        return jsonify({"code": 400, "message": "Drug dispense unsuccessful. Input should be in JSON."}), 400 # Bad Request

def processLog(order):
    print("Recording a log:")
    print(order)
    print() # print a new line feed as a separator


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
    app.run(host='0.0.0.0', port=5003, debug=True)