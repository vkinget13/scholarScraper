from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()

# Open Google
driver.get("https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=%22Brabantse+wouden%22%7C%22Heverleebos%22&btnG=")
time.sleep(2)
#each result is an element

while True:
    searchResults = driver.find_elements(By.CSS_SELECTOR,"div.gs_or")
#Filter through each results
    for i in searchResults:
        print("------------------")
        print(i.text)
    #title = i.find_element(By.CSS_SELECTOR, ".gs_rt").text
    #print("XXXX")
    #print(title)
        print("- - - - - - - ")
# extract pdf if it exists
        pdfLinkElement = i.find_elements(By.CSS_SELECTOR, ".gs_or_ggsm")
        if pdfLinkElement:
            pdfUrl = pdfLinkElement[0].get_attribute("href")
            print("PDF url: ", pdfUrl)
#extract the citation of each result
        try:
            citeButton = i.find_element(By.CSS_SELECTOR,"a.gs_or_cit")
            actions = ActionChains(driver)
            actions.move_to_element(citeButton).perform()
            citeButton.click()
            time.sleep(1)
#close the citation pop up window 
            box = driver.find_element(By.CSS_SELECTOR,"div#gs_cit-bdy")
            print(box.text)
            close = driver.find_element(By.CSS_SELECTOR,"a#gs_cit-x")
            time.sleep(1)
            close.click()
            time.sleep(1)
        except Exception as e:
            print("error getting citation {e}")
#go to next page using the next button 
    try:
        nextButton = driver.find_elements(By.CSS_SELECTOR,'td a b')
        print(len(nextButton))
        nextButton.click()
    except Exception as e:
        print("no more pages")
        break




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
