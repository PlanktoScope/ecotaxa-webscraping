############################################ Imports ################################################
import requests
from bs4 import BeautifulSoup
import csv


####################################### Global variables ############################################
# The URL of the page to scrape
url = 'https://ecotaxa.obs-vlfr.fr/objectdetails/513442748?w=1136&h=655' #'https://ecotaxa.obs-vlfr.fr/prj/10467'
metadata_to_save = ["Original Object ID", "height", "width", "bx", "by", "x", "y", "bounding_box_area"]
metadata_path = 'Webscraping/Data/metadata.csv'


################################# Fetch the web page for metadata ###################################
# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser') #"""<div><ul class="nav nav-tabs" role="tablist">...</div>"""

# Find the 'tabdobj' division which contains the metadata table
tabdobj_div = soup.find('div', id='tabdobj')

# Now, find the table within this div
metadata_table = tabdobj_div.find('table', {'data-table': 'object'})

# Assuming the metadata like 'x' and 'y' pixels are stored in a table under 'tabdobj'
metadata = {}

# Iterate through table rows (<tr>) to find and extract metadata
for row in metadata_table.find_all('tr'):
    cells = row.find_all('td')
    # Assuming each piece of metadata is contained within <td> tags
    for i in range(0, len(cells), 2):  # Step by 2 since key and value are in pairs
        key = cells[i].text.strip() #strip=True
        value = cells[i+1].text.strip()
        metadata[key] = value
        print(f"{key}: {value}")


###################################### Save scraped metadata ########################################
# Save Original Object ID, height, width, bx, by, x, y, and bounding_box_area to a csv file
with open(metadata_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(metadata_to_save)
    writer.writerow([metadata[var] for var in metadata_to_save])
