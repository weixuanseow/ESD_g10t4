#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/error", methods=['POST'])
def receiveError():
    data = request.get_data() # get any data in the request as the error message
    processError(data)
    # HTTP reply
    return jsonify({"code": 200, "data": 'OK. Error log printed.'}), 200 # return message is not used in our case

def processError(errorMsg):
    print("Printing the error message:")
    try:  # check if valid JSON
        error = json.loads(errorMsg)
        print("--JSON:", error)
    except Exception as e:
        print("--INVALID JSON:", e)
        print("--DATA:", errorMsg)
    print() # print a new line feed as a separator


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is flask for " + os.path.basename(__file__) + ": processing errors ...")
    app.run(host='0.0.0.0', port=5004, debug=True)
