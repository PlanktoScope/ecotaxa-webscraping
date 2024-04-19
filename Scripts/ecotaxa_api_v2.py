############################################################################################
# Imports
############################################################################################
import requests
import json
import csv
from tqdm import tqdm
import pandas as pd

############################################################################################
# Global variables & functions 
############################################################################################
# Define the base URL and project ID
api_url = "https://ecotaxa.obs-vlfr.fr/api"
project_id = 12053  # Example of a project ID

# The specific endpoint for querying object sets within a project
project_endpoint_url = f"{api_url}/object_set/{project_id}/query"

# The details (filename & path) to save the metadata
metadata_file_json = "metadata_objects_missing.json"
metadata_file_csv = "metadata_objects_missing_v1.csv"
metadata_path = f"Webscraping/Data/{metadata_file_json}"

# Function to flatten nested dictionaries in the object details response
def flatten(d, parent_key='', sep='_'): #existing_keys=set()
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            #for i, item in enumerate(v):
                #items.extend(flatten(item, f"{new_key}_{i}", sep=sep).items())
            for item in v:
                items.extend(flatten(item, f"{new_key}", sep=sep).items())
        else:
            """if new_key not in existing_keys:
                items.append((new_key, v))
                existing_keys.add(new_key)"""
            items.append((new_key, v))
    return dict(items)

############################################################################################
# Authentication to obtain JSON Web Token (JWT) 
############################################################################################
# EcoTaxa login endpoint
login_url = f"{api_url}/login"

# Indicate the Ecotaxa credentials
credentials = {
    "username": "x", # email
    "password": "1234" # password
}

# Make the login request
response = requests.post(login_url, json=credentials)

if response.status_code == 200:
    # Get the JWT response
    jwt_token = response.json() #.get('access_token')
    print("JWT Token:", jwt_token)
else:
    print("Failed to authenticate:", response.status_code, response.text)

# Prepare headers, including authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt_token}"
}

############################################################################################
# Fetch the API for object identifiers & store
############################################################################################
# Define other parameters as per our requirement
payload = {
    "fields": "obj.objid",
    "order_field": "obj.objid",  # Example ordering field
    "window_start": 0,  # Assuming we want to start from the first result
    "window_size": 1  # Number of results we want to fetch in one go
}

# Send the POST request
response_ids = requests.post(project_endpoint_url, headers=headers, data=json.dumps(payload))

# Check the response_ids
if response_ids.status_code == 200:
    data = response_ids.json()
    object_ids = data["object_ids"]
    print(f"Done extracting project's object IDs")
    #print(type(data), data["object_ids"])
    #print(json.dumps(data, indent=4)) # Print the response_ids data
else:
    print("Failed to retrieve data:", response.status_code)

############################################################################################
# Fetch the API for object metadata & save
############################################################################################
# Define an option to save the metadata in JSON or CSV format
save_option = metadata_path.endswith('.json')

# Open the metadata file in append mode
with open(metadata_path, 'a', newline='') as file: #newline='' #lineterminator=''
    # Loop through each object ID to retrieve its detailed information
    for object_id in tqdm(object_ids, desc="Fetching Object Metadata"):
        # Construct the URL for the specific object
        object_endpoint_url = f"{api_url}/object/{object_id}"
        
        # Make the GET request
        response_meta = requests.get(object_endpoint_url, headers=headers)
        
        # Check if the request was successful
        if response_meta.status_code == 200:
            object_details = response_meta.json()
            #print(f"Object ID {object_id}:")
            #print(object_details)  # Or process the object details as needed

            # Flatten the object details
            flattened_details = flatten(object_details)

            # Write the object ID and metadata to the file
            if save_option:
                file.write(f"{json.dumps(flattened_details)}\n") #object_details

            else:
                # Open CSV file for writing
                csv_writer = csv.DictWriter(file, fieldnames=flattened_details.keys())

                # Write header if the file is empty
                if file.tell() == 0:
                    csv_writer.writeheader()

                # Write flattened object details to CSV
                csv_writer.writerow(flattened_details)
            
            print(f"Data done for object ID {object_id}")
        else:
            print(f"Failed to retrieve details for object ID {object_id}: {response.status_code}")

print("Data saved successfully.")

############################################################################################
# Cleaning & dropping columns that contain missing values
############################################################################################
if not save_option:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(metadata_path)

    # Drop rows with missing values
    df.dropna(axis=1, inplace=True)

    # Drop the "sunpos" column as it contains only blank spaces
    df.drop(columns=["sunpos"], inplace=True)

    # Rewrite the CSV file
    clean_meta_path = metadata_path.replace(metadata_file_csv, "metadata_objects_cleaned_v1.csv")
    df.to_csv(clean_meta_path, index=False)

    print("Clean csv file saved successfully.")
