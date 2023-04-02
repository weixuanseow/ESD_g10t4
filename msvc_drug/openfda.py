import requests

def check_interactions(medicine_names):
    interactions = []
    for i, drug1 in enumerate(medicine_names):
        for drug2 in medicine_names[i+1:]:
            # Set the OpenFDA API endpoint and search parameters
            url = f'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:{drug1}+AND+patient.drug.openfda.generic_name:{drug2}&limit=10'

            # Send request to the OpenFDA API
            response = requests.get(url)
            data = response.json()

            # Add drug pair tuple
            if 'error' in data:
                print("No interactions found")
            else:
                interactions.append((drug1, drug2))

    return interactions