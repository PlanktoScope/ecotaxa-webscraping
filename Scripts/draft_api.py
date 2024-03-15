import requests

# Placeholder URL and project ID - replace with actual values and endpoint
project_id = "YOUR_PROJECT_ID"
api_url = f"https://ecotaxa.obs-vlfr.fr/api/projects/{project_id}/objects"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # If authentication is required
}

response = requests.get(api_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Example of processing the data - adjust according to actual data structure
    for object in data:
        print(f"Object ID: {object['id']}, X: {object['x_pos']}, Y: {object['y_pos']}")
else:
    print("Failed to retrieve data:", response.status_code)

#########################################################################################
    
#########################################################################################
    
"""# Open the metadata file in append mode
                with open(metadata_path, 'a', newline='') as file:
                    # Create a CSV writer object
                    writer = csv.writer(file)

                    # Write the header if the file is empty
                    if file.tell() == 0:
                        writer.writerow(object_details.keys())

                    # Write the metadata to the file
                    writer.writerow(object_details.values())"""