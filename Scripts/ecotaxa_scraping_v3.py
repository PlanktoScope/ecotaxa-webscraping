############################################ Imports ################################################
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

############################################################################################################
# Using requests and BeautifulSoup won't be sufficient because this content is likely loaded via JavaScript, 
# and requests fetches only the static HTML content of the page.
############################################################################################################


####################################### Global variables ############################################
project_path = "https://ecotaxa.obs-vlfr.fr/prj/10467"
metadata_to_save = ["Original Object ID", "height", "width", "bx", "by", "x", "y", "bounding_box_area"]
metadata_path = 'Webscraping/Data/global_metadata.csv'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) # Define the web driver


################################# Fetch the web page for metadata ###################################
# Navigate to the URL
driver.get(project_path)

# Wait for the popup with id="PopupDetails" to be visible
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "PopupDetails"))
)

# Now that the popup is visible, you can proceed to interact with the metadata table
# Find the table within the popup
popup_details = driver.find_element(By.ID, "PopupDetails")
#print(popup_details, type(popup_details)) #✔

# Locate the metadata table
metadata_table = driver.execute_script("return document.querySelector('table[data-table=\"object\"]');")
#metadata_table = popup_details.find_element(By.ID, "tabdobj")
#metadata_table = popup_details.find_element(By.TAG_NAME, "table")
#metadata_table = popup_details.find_element(By.CSS_SELECTOR, 'table[data-table="object"]')
#print(metadata_table, type(metadata_table)) #✔

# Interact with or scrape data from metadata_table goes here
metadata = {}

# Iterate through table rows (<tr>) to find and extract metadata
for row in metadata_table.find_elements(By.TAG_NAME, "tr"):
    cells = row.find_elements(By.TAG_NAME, 'td')
    # Assuming each piece of metadata is contained within <td> tags
    for i in range(0, len(cells), 2):  # Step by 2 since key and value are in pairs
        key = cells[i].text.strip() #strip=True
        value = cells[i+1].text.strip()
        metadata[key] = value
        print(f"{key}: {value}")

# Don't forget to close the driver after your scraping job is done
driver.quit()

###################################### Save scraped metadata ########################################
# Save Original Object ID, height, width, bx, by, x, y, and bounding_box_area to a csv file
with open(metadata_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(metadata_to_save)
    writer.writerow([metadata[var] for var in metadata_to_save])

