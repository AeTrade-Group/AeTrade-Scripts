import requests
import base64

def create_option_if_not_exists(api_url, headers, option_name):
    # Check if the option exists
    response = requests.get(f"{api_url}/options?filter=name:eq:{option_name}", headers=headers)
    if not response.json()['options']:
        # Create the option
        option_data = {
            "name": option_name,
            "code": option_name
        }
        response = requests.post(f"{api_url}/options", json=option_data, headers=headers)
        if response.status_code == 201:
            return response.json()['response']['uid']
        else:
            raise Exception(f"Failed to create option {option_name}: {response.text}")
    return response.json()['options'][0]['id']

def check_or_create_option_set(api_url, headers, option_set_name, options):
    # Create options if they don't exist
    option_ids = [create_option_if_not_exists(api_url, headers, option) for option in options]

    # Check if the option set exists
    response = requests.get(f"{api_url}/optionSets?filter=name:eq:{option_set_name}", headers=headers)
    if not response.json()['optionSets']:
        # Create the option set
        option_set_data = {
            "name": option_set_name,
            "valueType": "TEXT",
            "options": [{"id": option_id} for option_id in option_ids]
        }
        response = requests.post(f"{api_url}/optionSets", json=option_set_data, headers=headers)
        if response.status_code == 201:
            return response.json()['response']['uid']
        else:
            raise Exception(f"Failed to create option set {option_set_name}: {response.text}")
    return response.json()['optionSets'][0]['id']

def create_tracked_entity_attribute(api_url, headers, attribute_name, value_type, description, short_name, option_set_id=None):
    attribute_data = {
        "name": attribute_name,
        "valueType": value_type,
        "description": description,
        "shortName": short_name,
        "aggregationType": "NONE",
        "domainType": "TRACKER",
        "optionSetValue": bool(option_set_id),
        "optionSet": {"id": option_set_id} if option_set_id else None
    }
    response = requests.post(f"{api_url}/trackedEntityAttributes", json=attribute_data, headers=headers)
    return response

api_url = 'YOUR_DHIS2_INSTANCE_API_URL'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()
}

# Create option set for Gender
gender_options = ['Male', 'Female', 'Other', 'Prefer not to say']
gender_option_set_id = check_or_create_option_set(api_url, headers, "Gender Option Set", gender_options)

# List of Tracked Entity Attributes to create with shortName
teas = [
    {"name": "Full Name", "valueType": "TEXT", "description": "Candidate's full name", "short_name": "FullName"},
    {"name": "Date of Birth", "valueType": "DATE", "description": "Candidate's date of birth", "short_name": "DOB"},
    {"name": "Gender", "valueType": "TEXT", "description": "Candidate's gender", "short_name": "Gender", "option_set_id": gender_option_set_id},
    {"name": "National ID Number", "valueType": "TEXT", "description": "Candidate's national ID number", "short_name": "NationalID"},
    {"name": "Email Address", "valueType": "EMAIL", "description": "Candidate's email address", "short_name": "Email"},
    {"name": "Phone Number", "valueType": "PHONE_NUMBER", "description": "Candidate's phone number", "short_name": "Phone"}
]

for tea in teas:
    response = create_tracked_entity_attribute(api_url, headers, tea['name'], tea['valueType'], tea['description'], tea['short_name'], tea.get('option_set_id'))
    if response.status_code == 201:
        print(f"Tracked Entity Attribute '{tea['name']}' created successfully.")
    else:
        print(f"Error creating Tracked Entity Attribute '{tea['name']}': {response.text}")

# Note: Replace 'YOUR_DHIS2_INSTANCE_API_URL', 'YOUR_USERNAME', and 'YOUR_PASSWORD' with your actual DHIS2 instance details.

