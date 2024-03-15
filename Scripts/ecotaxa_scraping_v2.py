import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as EdgeService #ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# URL of the page to scrape
url = 'https://ecotaxa.obs-vlfr.fr/prj/10467'

# Setup the WebDriver (assuming ChromeDriver)
#driver = webdriver.Chrome('/path/to/chromedriver')
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

# Navigate to the URL
driver.get(url)

# Wait for dynamic content to load or interact with the website as necessary
# For example, clicking a button to open the popup window containing the metadata

# Once the dynamic content is loaded, you can now access the page source
page_source = driver.page_source

# Now use BeautifulSoup to parse the HTML content of the page
soup = BeautifulSoup(page_source, 'html.parser') #"""<div><ul class="nav nav-tabs" role="tablist">...</div>"""

# Find the popup window containing the metadata table
# Assuming the popup window is a div with class 'popup-class'
popup_div = soup.find('div', class_='popup-class')

# Find the 'tabdobj' division which contains the metadata table
tabdobj_div = popup_div.find('div', id='tabdobj') #soup

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

# Access the x and y values directly
x_pixels = metadata.get('x')
y_pixels = metadata.get('y')

