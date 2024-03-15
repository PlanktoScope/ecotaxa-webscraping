import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

############################################ Imports ################################################

############################################################################################################
# Using requests and BeautifulSoup won't be sufficient because this content is likely loaded via JavaScript, 
# and requests fetches only the static HTML content of the page.
############################################################################################################


####################################### Global variables ############################################
metadata_to_save = ["Original Object ID", "height", "width", "bx", "by", "x", "y", "bounding_box_area"]
metadata_path = 'Webscraping/Data/global_metadata_CapenaxFairScope.csv'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) # Define the web driver


################################# Fetch the web page for metadata ###################################
# Navigate to the URL
driver.get("https://ecotaxa.obs-vlfr.fr/prj/10467")

# Wait for the popup with id="PopupDetails" to be visible
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "PopupDetails"))
)

# Now that the popup is visible, you can proceed to interact with the metadata table
# Find all the popup buttons on the page
popup_buttons = driver.find_elements(By.CLASS_NAME, "modal")

# Index or counter of the popup buttons
popup_index = 0

# Iterate through each popup button
for button in popup_buttons:
    # Click on the popup button to open the popup
    button.click()
    
    # Wait for the popup with id="PopupDetails" to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "PopupDetails"))
    )
    
    # Find the table within the popup
    popup_details = driver.find_element(By.ID, "PopupDetails")
    
    # Locate the metadata table
    metadata_table = driver.execute_script("return document.querySelector('table[data-table=\"object\"]');")
    
    # Interact with or scrape data from metadata_table goes here
    metadata = {}
    
    # Iterate through table rows (<tr>) to find and extract metadata
    for row in metadata_table.find_elements(By.TAG_NAME, "tr"):
        cells = row.find_elements(By.TAG_NAME, 'td')
        # Assuming each piece of metadata is contained within <td> tags
        for i in range(0, len(cells), 2):  # Step by 2 since key and value are in pairs
            key = cells[i].text.strip()
            value = cells[i+1].text.strip()
            metadata[key] = value
            print(f"{key}: {value}")
    
    """# Don't forget to close the popup after scraping the metadata
    close_button = popup_details.find_element(By.CLASS_NAME, "close-button")
    close_button.click()"""
    
    # Save metadata variables to a row in the csv file
    with open(metadata_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([metadata[var] for var in metadata_to_save])

# Don't forget to close the driver after your scraping job is done
driver.quit()
