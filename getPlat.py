from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import csv
import random
import time
import copy
import argparse

explanation = 'This program runs RIAA datascraping for all awards except Gold.'
parser = argparse.ArgumentParser(description=explanation)
parser.add_argument("-s", "--servicefile", help="file for chromeDriver", required=True)
parser.add_argument("-f", "--firefox", help="action chooses firefox driver", action='store_true')
parser.add_argument("-o", "--outputfile", help="output file for csv")
args = parser.parse_args()
filepath = args.outputfile
if not filepath:
    filepath = 'riaaAwards.csv'
servicefile = args.servicefile
#Driver allows selenium to grab data from site
driverService = Service(servicefile)
if args.firefox:
    driver = webdriver.Firefox(service=driverService)
else:
    driver = webdriver.Chrome(service=driverService)
PATIENCE_TIME = 60

# go to specific site -- this starts at the very beginning, before the first
# award was given to ensure all the awards are grabbed.
driver.get("https://www.riaa.com/gold-platinum/?tab_active=default-award&ar=&ti=&lab=&genre=&format=&date_option=release&from=&to=&award=P&type=&category=&adv=SEARCH#search_section")
driver.implicitly_wait(0.5)

def findClassEl(element,driver):
    actionDone = False
    count = 0
    while not actionDone:
        if count == 3:
            raise Exception("Cannot found element %s after retrying 3 times.\n"%element)
            break
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                    EC.visibility_of_element_located((By.ID, element)))
            actionDone = True
        except:
            count += 1
    time.sleep(random.randint(1,5)*0.1)
    return element

# Grab table using ID
table = driver.find_element(By.ID, "search-award-table")

header_row = ["AWARD", "ARTIST", "TITLE", "CERTIFICATION DATE", "LABEL", "FORMAT", " ", "PREV CERTIFICATION DATE & AWARD"]
data_arr = []
load_button_path = '//*[@id="content"]/section/div[4]/div/div[1]/div/div/a'
counter = 0
print("begin scrolling")
while True:
    try:
        loadMoreButton = driver.find_element(By.XPATH, load_button_path)
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(2)
        counter += 1
    except Exception as e:
        print("exception")
        print(e)
        break
print("Scrolling done. Pulling data.")

# This is assuming that each row will have the same set of information.
# TODO: change if this isnt the case
with open(filepath, 'a+') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(header_row)
    for tr in table.find_elements(By.CLASS_NAME, "table_award_row"):
        more_details = False
        data_row = []
        data_row.append("PLATINUM")
        id_num = tr.get_attribute("id").split('_')[1]
        for td in tr.find_elements(By.TAG_NAME, 'td'):
            if td.get_attribute("class") == "others_cell format_cell":
                text = td.text.split("\n")
                data_row.append(text[0])
            elif td.get_attribute("class") != "award_cell":
                data_row.append(td.text)
            if td.get_attribute("class") == "others_cell format_cell":
                td.find_element(By.LINK_TEXT, "MORE DETAILS").click()
                time.sleep(2)
                more_details = True
        if more_details:
            class_name = "recent_" + id_num + "_detail"
            try:
                findClassEl(class_name,driver)
            except:
                print("Error. Code continues and skips " + class_name)
            else:
                extra_info = driver.find_element(By.ID, class_name)
                prev_cert_date = []
                for td in extra_info.find_elements(By.TAG_NAME, 'td'):
                    if td.get_attribute("class") == "col-md-5":
                        prev_cert_date.append(td.text)
                for prev_date in prev_cert_date:
                    new_row = copy.deepcopy(data_row)
                    dates_and_awards = prev_date.split(" | ")
                    new_row[0] = dates_and_awards[0].upper()
                    new_row[3] = dates_and_awards[1]
                    filewriter.writerow(new_row)
                more_details = False
print("Ending program")

driver.quit()
