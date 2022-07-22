# import libraries
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import pandas as pd

def getContent(e):
    start = e.get_attribute('innerHTML')
    # remove HTML tags from our content if it exists.
    soup = BeautifulSoup(start, features="lxml")
    return soup.get_text()


DRIVER_PATH = "E:/python/ChromeDriver/chromedriver"
URL = "https://www.rew.ca/rentals"

browser = webdriver.Chrome(service=Service(DRIVER_PATH))
browser.get(URL)

# Give the browser time to load all content.
time.sleep(1)

SEARCH_TERM = "vancouver"
search = browser.find_element(By.CSS_SELECTOR,"#listing_search_query")
search.send_keys(SEARCH_TERM)

# Find the search button - this is only enabled when a search query is entered
button = browser.find_element(By.CSS_SELECTOR,".rewicon-search")
button.click()  # Click the button.
time.sleep(3)

# initiate an empty list to store extracted data
costList = []
bedroomList = []
bathroomList = []
sizeList = []
addressList = []
neighbourhoodList = []
cityList = []
typeList = []
# count the number of rentals
countItem = 0
# looping 3 pages
page = 3
for i in range(0,page):

    # count the number of item in a page
    # search for the cost element
    costContent = browser.find_elements(by=By.CSS_SELECTOR, value='.displaypanel-body')
    for e in costContent:
        rawString = getContent(e)
        rawString = re.sub(r"[\n]", "*", rawString)
        costArray = rawString.split('***')
        cost = costArray[0]
        cost = re.sub("[^0-9]", "", cost)
        costList.append(cost)
        countItem += 1

    addressContent = browser.find_elements(by=By.CSS_SELECTOR, value='.hidden-xs+ .displaypanel-section')
    for e in addressContent:
        rawString = getContent(e)
        # cleaning process:
        # Remove hidden characters for new lines and substitute with *.
        rawString = re.sub(r"[\n]", "*", rawString)
        addressArray = rawString.split('**')
        address = addressArray[0]
        cityArray = addressArray[1].split('*')
        neighbourhood = cityArray[0]
        city = cityArray[1]
        addressList.append(address)
        cityList.append(city)
        neighbourhoodList.append(neighbourhood)

    detailsContent = browser.find_elements(by=By.CSS_SELECTOR, value='.clearfix .inlinelist')
    for e in detailsContent:
        rawString = getContent(e)
        # Remove hidden characters for new lines and substitute with *.
        rawString = re.sub(r"[\n]", "*", rawString)
        detailsArray = rawString.split("*")
        bedroom = detailsArray[0]
        bedroom = re.sub("[^0-9]", "",bedroom)
        bathroom = detailsArray[1]
        bathroom = re.sub("[^0-9]", "",bathroom)
        size = detailsArray[2]
        size = re.sub("[^0-9]", "", size)
        bedroomList.append(bedroom)
        bathroomList.append(bathroom)
        sizeList.append(size)

    typeContent = browser.find_elements(by=By.CSS_SELECTOR, value='.hidden-xs .displaypanel-info')
    for e in typeContent:
        type = getContent(e)
        typeList.append(type)

    # go to the next page
    nextButton = browser.find_element(By.CSS_SELECTOR,".rewicon-play-o")
    nextButton.click()
    time.sleep(3)

# create a data frame
zippedList = list(zip(costList,bedroomList,bathroomList,sizeList,addressList,
                      neighbourhoodList,cityList,typeList))
df = pd.DataFrame(zippedList,
                  columns=['monthly cost','address','neighbourhood','city',
                           'bedroom','bathroom','size(sf)','type'])
#print(df)

# save data frame in a csv file
df.to_csv('rentalData.csv')



