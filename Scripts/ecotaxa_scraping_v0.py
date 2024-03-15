import requests
from bs4 import BeautifulSoup

############################################################################################################
# Using requests and BeautifulSoup won't be sufficient because this content is likely loaded via JavaScript, 
# and requests fetches only the static HTML content of the page.
############################################################################################################

# The URL of the page to scrape
url = 'https://ecotaxa.obs-vlfr.fr/prj/10467'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements containing the metadata (this is a placeholder and needs to be updated)
metadata_elements = soup.find_all('div', class_='metadata-class')  # Update 'div' and 'metadata-class' accordingly !!

# Extract and print the desired metadata
for element in metadata_elements:
    x_pixels = element.find('span', class_='x-pixels-class').text  # Update 'span' and 'x-pixels-class' !!
    y_pixels = element.find('span', class_='y-pixels-class').text  # Update 'span' and 'y-pixels-class' !!
    print(f'X Pixels: {x_pixels}, Y Pixels: {y_pixels}')

