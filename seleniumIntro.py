from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from datetime import datetime
from time import time, sleep
import requests
import pandas



def createDatasetDetailsCSV():
    pandas.DataFrame(columns = ["File Name", "Date", "Time"]).to_csv("./DatasetDetails.csv" , index = False, header = True)

def addNameDateTimeDetailsToCSV():
    lastFileName = len(pandas.read_csv("./DatasetDetails.csv"))
    date, time = str(datetime.now()).split()
    hour, minute, _ = time.split(":")
    
    info = \
    {
        "File Name" : str(lastFileName + 1),
        "Date" : date,
        "Time" : ":".join([hour, minute])
    }

    pandas.DataFrame(info , index = [0]).to_csv("./DatasetDetails.csv", mode = "a", index = False, header = False)

def closePopUpWindow(chrome : WebDriver):
    closeButton = chrome.find_element(
        By.ID, "GuideMedical"
    ).find_element(
        By.CSS_SELECTOR , 'button[aria-label="Close"]'
    )

    closeButton.click()

def getImageURL(chrome):
    return chrome.find_element(
        By.ID, "imgHeader"
    ).get_attribute(
        "src"
    )

def saveImage(imageURL):
    photoPath = f'./Dataset/{len(pandas.read_csv("./DatasetDetails.csv"))}.jpg'

    with open(photoPath , 'wb') as handler:
        handler.write(requests.get(imageURL).content)


startTime = time()
waitPeriodInMinutes = 30

options = Options()
options.headless = True
chrome = webdriver.Chrome(".\chromedriver", options = options)
chrome.implicitly_wait(5)

createDatasetDetailsCSV()
chrome.get("https://airnow.tehran.ir/")

while(True):
    chrome.refresh()
    closePopUpWindow(chrome)
    
    addNameDateTimeDetailsToCSV()
    imageURL = getImageURL(chrome)
    saveImage(imageURL)
    print("Log: New Picture Scrapped At " + str(datetime.now()))

    sleep( (waitPeriodInMinutes * 60.0) - ((time() - startTime) % (waitPeriodInMinutes * 60.0)) )
    