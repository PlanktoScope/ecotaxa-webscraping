############################################ Imports ################################################
import requests
import json
import csv


####################################### Global variables ############################################
# Specify project ID
project_id = 4824
api_url = f"https://ecotaxa.obs-vlfr.fr/api/object_set/{project_id}/summary"


################################# Fetch the API for project metadata ###################################
# Assuming token-based authentication
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

# Replace payload with any required parameters for the query
payload = {}

response = requests.post(api_url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    # Process your data here
    print(json.dumps(data, indent=4))
else:
    print("Failed to retrieve data:", response.status_code)
