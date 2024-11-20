from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import openpyxl

# Path to your Chrome user profile
options = webdriver.ChromeOptions()
# The r means that the string is to be treated as a raw string,
# which means all escape codes will be ignored.
user_data_dir = r'C:\Users\VincentKinget\AppData\Local\Google\Chrome\User Data' 
# User's data path
options.add_argument('--user-data-dir='+user_data_dir)
# Profile directory
options.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(options=options)
# Open Google
driver.get("https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=%22brabantse+wouden%22&oq=%22Brab")
time.sleep(2)


#create an excel workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Scholar Data"
ws.append(["Result text", "PDF URL", "Citation text"])  # header

#each result is an element
while True:
    searchResults = driver.find_elements(By.CSS_SELECTOR,"div.gs_or")
#Filter through each results
    for i in searchResults:
        print("------------------")
        resultText = i.text
        print(resultText)
    #title = i.find_element(By.CSS_SELECTOR, ".gs_rt").text
    #print("XXXX")
    #print(title)
        print("- - - - - - - ")
# extract pdf if it exists
        pdfLinkElement = i.find_elements(By.CSS_SELECTOR, ".gs_or_ggsm")
        if pdfLinkElement:
            pdfUrl = pdfLinkElement[0].get_attribute("href")
            print("PDF url: ", pdfUrl)
        else:
            pdfUrl = "N/A"
#extract the citation of each result
        try:
            citeButton = i.find_element(By.CSS_SELECTOR,"a.gs_or_cit")
            actions = ActionChains(driver)
            actions.move_to_element(citeButton).perform()
            citeButton.click()
            time.sleep(1)

            box = driver.find_element(By.CSS_SELECTOR,"div#gs_cit-bdy")
            citationText = box.text
            print("Citation: ", citationText)
            close = driver.find_element(By.CSS_SELECTOR,"a#gs_cit-x")
            time.sleep(1)
            close.click()
            time.sleep(1)
        except Exception as e:
            print("error getting citation {e}")

        #append data to excel worksheet
        ws.append([resultText, pdfUrl, citationText])

    try:
        nextButton = driver.find_elements(By.CSS_SELECTOR,'td a b')
        print(len(nextButton))
        nextButton = nextButton[0]
        nextButton.click()
    except Exception as e:
        print("no more pages")
        break

#saving excel file
    excelName = "NPBW_Onderzoek_inventaris.xlsx"
    wb.save(excelName)




#go to the next page of results
#next = driver.find_elements(By.CSS_SELECTOR,'td a b')
#print(len(next))
#next = next[0]
#actions.move_to_element(next).perform()
#next.click()


#print(driver.title)

# Find the search box using its name attribute value
# search_box = driver.find_element(By.NAME, "q")
# print(search_box)

# # Type 'Selenium Python' in the search box
# search_box.send_keys("Selenium Python")

# Simulate pressing the Enter key
#search_box.send_keys(Keys.RETURN)

# Wait for a few seconds to see the results
time.sleep(10)

# Close the browser
driver.quit()