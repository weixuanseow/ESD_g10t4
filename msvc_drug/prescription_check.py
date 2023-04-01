from flask import Flask, request, jsonify
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
        interactions = []
        for i, drug1 in enumerate(medicine_names):
            for drug2 in medicine_names[i+1:]:
                # Set the OpenFDA API endpoint and search parameters
                url = f'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:{drug1}+AND+patient.drug.openfda.generic_name:{drug2}&limit=10'

            # Send request to the OpenFDA API
                response = requests.get(url)
                data = response.json()
                # print(data)

                # Add drug pair tuple
                if 'error' in data:
                    print("No interactions found")
                else:
                    interactions.append((drug1, drug2))


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
