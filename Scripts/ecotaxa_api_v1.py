############################################ Imports ################################################
import requests
import json
import csv

####################################### Global variables ############################################
# Define the base URL and project ID
api_url = "https://ecotaxa.obs-vlfr.fr/api"
project_id = 12053  # Example of a project ID

# The specific endpoint for querying object sets within a project
object_endpoint_url = f"{api_url}/object_set/{project_id}/query" #https://ecotaxa.obs-vlfr.fr/api/docs#/objects/get_object_set

# The details (filename & path) to save the metadata
metadata_file = "first_ecotaxtapi.json"
metadata_path = f"Webscraping/Data/{metadata_file}"

########################### Authentication to obtain JSON Web Token (JWT) ###########################
# EcoTaxa login endpoint
login_url = f"{api_url}/login" #https://ecotaxa.obs-vlfr.fr/api/docs#/authentification/login

# Indicate the Ecotaxa credentials
credentials = {
    "username": "wassim@fairscope.com", #Wassim Chakroun
    "password": "6902.xhlzO!"
}

# Make the login request
response = requests.post(login_url, json=credentials)

if response.status_code == 200:
    # Get the JWT response
    jwt_token = response.json() #.get('access_token')
    print("JWT Token:", jwt_token)
else:
    print("Failed to authenticate:", response.status_code, response.text)

################################ Fetch the API for project metadata #################################
# Prepare headers, including authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt_token}"
}

# Define the object-related fields with the 'obj.' prefix
object_fields = [
    "obj.acquisid", "obj.classif_auto_id", "obj.classif_auto_score", 
    "obj.classif_auto_when", "obj.classif_crossvalidation_id", "obj.classif_id", 
    "obj.classif_qual", "obj.classif_who", "obj.classif_when", "obj.complement_info", 
    "obj.depth_max", "obj.depth_min", "obj.latitude", "obj.longitude", 
    "obj.objdate", "obj.object_link", "obj.objid", "obj.objtime", 
    "obj.orig_id", "obj.random_value", "obj.similarity", "obj.sunpos"
]

# Define the image-related fields with the 'img.' prefix
image_fields = [
    "img.file_name", "img.height", "img.imgid", "img.imgrank", 
    "img.orig", "img.objid", "img.thumb_file_name", "img.thumb_height", 
    "img.thumb_width", "img.width"
]

# Combine all fields into a single list
all_fields = object_fields + image_fields

# Convert the list into a comma-separated string
fields_string = ",".join(all_fields)

# Define other parameters as per your requirement
payload = {
    "fields": fields_string,
    #"order_field": "obj.objid",  # Example ordering field
    "window_start": 0,  # Assuming we want to start from the first result
    "window_size": 10  # Number of results we want to fetch in one go
}

# Send the POST request
response = requests.post(object_endpoint_url, headers=headers, data=json.dumps(payload))

##################################### Store scraped metadata #######################################
# Check the response
if response.status_code == 200:
    data = response.json()
    #print(json.dumps(data, indent=4)) # Print the response data
    with open(metadata_path, 'w') as file:
        json.dump(data, file, indent=4)
    print("Data saved successfully.")
else:
    print("Failed to retrieve data:", response.status_code)
