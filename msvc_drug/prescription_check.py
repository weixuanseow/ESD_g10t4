from flask import Flask, request, jsonify
from collections import Counter
import requests
import json

############ compare drugs & allergy
@app.route('/check-interaction', methods=['GET'])
def check_interaction():
    # Get prescription details and patient allergies from request
    # define in prescribe medicine complex microservice
    prescription = json.loads(request.json['medicine'])['medicine']  # check on complex whether it will be list of medicines
    allergies = json.loads(request.json['allergies'])['allergies']

    # check if prescription exists in allergies
    allergic_to = set(prescription).intersection(set(allergies))
    if allergic_to:
        return jsonify(
            {
                'error': f'Patient is allergic to {", ".join(allergic_to)}'
            }
        )
    else:
        interactions = set()
        for i, drug1 in enumerate(prescription):
            for drug2 in prescription[i+1:]:
                # Set the OpenFDA API endpoint and search parameters
                url = f'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:"{drug1}"+AND+patient.drug.openfda.generic_name:"{drug2}"&limit=10'

            # Send a request to the OpenFDA API and check for errors
                response = requests.get(url)
                response.raise_for_status()

                # Extract the reaction terms from the API response
                data = response.json()
                reactions = {item['term'] for item in data['results']}

                # Add the drug pair tuple with reaction
                if reactions:
                    interactions.add((drug1, drug2, ', '.join(reactions)))

        # If interactions were found, return the drug pairs and their reactions
        if interactions:
            # sort according to length of interaction so that pair of drugs with most reactions appear first
            sorted_interactions = sorted(interactions, key=lambda x: len(x[2]), reverse=True)
            return jsonify(
                {
                    'interactions': [{'drugs': f'{pair[0]}, {pair[1]}', 'reactions': pair[2]} for pair in sorted_interactions]
                }
            )
        
        # If no interactions were found, return an error message
        else:
            return jsonify(
                {
                    'error': 'Patient is not allergic to the prescribed medication and there are no adverse interactions indicated from OpenFDA API'
                }
            )

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage prescriptions ...")
    app.run(host='0.0.0.0', port=5002, debug=True)
