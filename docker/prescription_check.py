from flask import Flask, request, jsonify
from openfda import check_interactions
import requests
import os

app = Flask(__name__)


############ compare drugs & allergy
@app.route('/check-interaction', methods=['GET'])
def check_interaction():
    data = request.get_json()
    patient_id = data['patient_id']
    medicine_names = data['medicine_names']
    allergies = data['allergies']

    # check if prescription exists in allergies
    allergic_to = set(medicine_names).intersection(set(allergies))
    print(allergic_to)
    if allergic_to:
        return jsonify(
            {
                'code': 400,
                'message': f'Patient is allergic to {", ".join(allergic_to)}. Please re-enter medicine!'
            }
        ),400
    else:
        interactions = check_interactions(medicine_names)
        
        # If interactions found, return the drug pairs
        if interactions:
             # convert list to string
            interaction_str = ', '.join([f'{drug1} and {drug2}' for drug1, drug2 in interactions])
            print(interaction_str)

            return jsonify(
                {
                    'code': 422,
                    'message': f'The following drugs have interactions: {interaction_str}. Please re-enter medicine!'
                }
            ),422
        
        # If no interactions were found, return an error message
        else:
            return jsonify(
                {
                    'code': 200,
                    'message': 'Patient is not allergic to the prescribed medication and there are no adverse interactions indicated from OpenFDA API'
                }
            ),200

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage prescriptions ...")
    app.run(host='0.0.0.0', port=5002, debug=True)
