import requests
import base64

def create_option_if_not_exists(api_url, headers, option_name):
    response = requests.get(f"{api_url}/options?filter=name:eq:{option_name}", headers=headers)
    if not response.json()['options']:
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
    option_ids = [create_option_if_not_exists(api_url, headers, option) for option in options]
    response = requests.get(f"{api_url}/optionSets?filter=name:eq:{option_set_name}", headers=headers)
    if not response.json()['optionSets']:
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

def create_data_element(api_url, headers, element_name, value_type, description, short_name, stage_id, option_set_id=None):
    element_data = {
        "name": element_name,
        "valueType": value_type,
        "description": description,
        "shortName": short_name,
        "aggregationType": "NONE",
        "domainType": "TRACKER",
        "programStages": [{"id": stage_id}],
        "optionSetValue": bool(option_set_id),
        "optionSet": {"id": option_set_id} if option_set_id else None
    }
    response = requests.post(f"{api_url}/dataElements", json=element_data, headers=headers)
    return response

api_url = 'YOUR_DHIS2_INSTANCE_API_URL'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()
}

# Creating option sets for fields with predefined choices
education_levels = ['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Other']
agricultural_sectors = ['Horticulture', 'Grains', 'Super Crops', 'Livestock (Poultry)', 'Other']
training_interests = ['Production', 'Agri-services', 'Agribusiness', 'Other']
financial_assistance_types = ['Loans', 'Grants', 'Investment', 'Other']

education_option_set_id = check_or_create_option_set(api_url, headers, "Education Level Option Set", education_levels)
sector_option_set_id = check_or_create_option_set(api_url, headers, "Agricultural Sector Option Set", agricultural_sectors)
training_interest_option_set_id = check_or_create_option_set(api_url, headers, "Training Interest Option Set", training_interests)
financial_assistance_option_set_id = check_or_create_option_set(api_url, headers, "Financial Assistance Type Option Set", financial_assistance_types)

# ID of the Candidate Onboarding program stage
stage_id = 'fCAMGXQcvCL'

# List of Data Elements to create for the Candidate Onboarding stage
data_elements = [
    {"name": "Highest Level of Education", "valueType": "TEXT", "description": "Candidate's highest level of education", "shortName": "EduLevel", "option_set_id": education_option_set_id},
    {"name": "Field of Study", "valueType": "TEXT", "description": "Candidate's field of study", "shortName": "FieldStudy"},
    {"name": "University/College Attended", "valueType": "TEXT", "description": "University or college attended by the candidate", "shortName": "UniCollege"},
    {"name": "Year of Graduation", "valueType": "TEXT", "description": "Year the candidate graduated", "shortName": "GradYear"},
    {"name": "Work Experience Description", "valueType": "LONG_TEXT", "description": "Description of candidate's work experience", "shortName": "WorkExp"},
    {"name": "Preferred Agricultural Sector", "valueType": "TEXT", "description": "Candidate's preferred agricultural sector", "shortName": "PrefAgriSector", "option_set_id": sector_option_set_id},
    {"name": "Reason for Choosing Sector", "valueType": "LONG_TEXT", "description": "Reason for choosing the preferred agricultural sector", "shortName": "ReasonSector"},
    {"name": "Previous Experience in Agriculture", "valueType": "TEXT", "description": "Candidate's previous experience in agriculture", "shortName": "PrevAgriExp"},
    {"name": "Technical Skills in Agriculture", "valueType": "LONG_TEXT", "description": "Technical skills related to agriculture", "shortName": "TechSkillsAgri"},
    {"name": "Interest in Additional Training", "valueType": "BOOLEAN", "description": "Interest in additional training", "shortName": "InterestTrain"},
    {"name": "Areas of Training Interest", "valueType": "TEXT", "description": "Areas of interest for additional training", "shortName": "TrainingAreas", "option_set_id": training_interest_option_set_id},
    {"name": "Interest in Entrepreneurship", "valueType": "BOOLEAN", "description": "Interest in entrepreneurship", "shortName": "InterestEntrepreneur"},
    {"name": "Business Ideas or Plans", "valueType": "LONG_TEXT", "description": "Description of any business ideas or plans", "shortName": "BusinessPlans"},
    {"name": "Need for Financial Assistance", "valueType": "BOOLEAN", "description": "Need for financial assistance", "shortName": "NeedFinancialAssist"},
    {"name": "Type of Financial Assistance Required", "valueType": "TEXT", "description": "Type of financial assistance required", "shortName": "TypeFinancialAssist", "option_set_id": financial_assistance_option_set_id},
    {"name": "Market Access Challenges", "valueType": "LONG_TEXT", "description": "Challenges in accessing markets", "shortName": "MarketChallenges"},
    {"name": "Short-term Career Goals", "valueType": "LONG_TEXT", "description": "Candidate's short-term career goals", "shortName": "ShortTermGoals"},
    {"name": "Long-term Career Goals", "valueType": "LONG_TEXT", "description": "Candidate's long-term career goals", "shortName": "LongTermGoals"},
    {"name": "Additional Information", "valueType": "LONG_TEXT", "description": "Any additional information or comments", "shortName": "AddInfo"},
    {"name": "Consent to Use Data", "valueType": "BOOLEAN", "description": "Consent to use data for the purposes of this program", "shortName": "ConsentUseData"},
    {"name": "Declaration", "valueType": "BOOLEAN", "description": "Declaration that the information provided is true and accurate", "shortName": "Declaration"}
]

for de in data_elements:
    response = create_data_element(api_url, headers, de['name'], de['valueType'], de['description'],  de['shortName'], stage_id, de.get('option_set_id'))
    if response.status_code == 201:
        print(f"Data Element '{de['name']}' created successfully.")
    else:
        print(f"Error creating Data Element '{de['name']}': {response.text}")

# Note: Replace 'YOUR_DHIS2_INSTANCE_API_URL', 'YOUR_USERNAME', and 'YOUR_PASSWORD' with your actual DHIS2 instance details.

