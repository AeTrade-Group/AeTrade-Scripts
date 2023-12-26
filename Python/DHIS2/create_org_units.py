import requests
import csv
from collections import defaultdict

# DHIS2 API credentials and base URL
api_url = "YOUR_DHIS2_INSTANCE_API_URL"
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

# Function to create an organizational unit in DHIS2
def create_org_unit(name, parent_id=None):
    """Create an organizational unit in DHIS2."""
    org_unit = {
        "name": name,
        "shortName": name[:50],  # DHIS2 requires a short name, max 50 characters
        "openingDate": "2023-01-01"  # A default opening date
    }
    if parent_id:
        org_unit["parent"] = {"id": parent_id}

    response = requests.post(
        f"{api_url}/organisationUnits",
        json=org_unit,
        auth=(username, password)
    )

    if response.status_code == 201:
        return response.json()['response']['uid']
    else:
        print(f"Failed to create {name}: {response.text}")
        return None

# Function to process the CSV and create the hierarchy
def process_csv_and_create_hierarchy(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        org_unit_ids = defaultdict(dict)  # Store IDs of created org units

        for row in reader:
            hierarchy = [x.strip() for x in row]  # Remove leading/trailing spaces

            # Iterate through each level and create org units
            parent_id = None
            for level, name in enumerate(hierarchy):
                if name not in org_unit_ids[level]:
                    org_unit_ids[level][name] = create_org_unit(name, parent_id)
                parent_id = org_unit_ids[level][name]

# Call the function with the CSV file path
process_csv_and_create_hierarchy('path_to_your_csv_file.csv')

