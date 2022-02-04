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

def retrieveAirQualityDetails(chrome : WebDriver):
    airQualityIndex = chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblAqi3h"
    ).get_attribute("innerHTML")

    mainPollutant = str(chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblAqi3hDesc"
    ).get_attribute("innerHTML")).split(":")[1]

    chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblMoreInfo1"
    ).click()

def addDetailsToCSV(chrome : WebDriver):
    lastFileName = len(pandas.read_csv("./DatasetDetails.csv"))
    date, time = str(datetime.now()).split()
    hour, minute, _ = time.split(":")

    retrieveAirQualityDetails(chrome)
    
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
    photoPath = f'./Dataset/{len(pandas.read_csv("./DatasetDetails.csv")) + 1}.jpg'

    with open(photoPath , 'wb') as handler:
        handler.write(requests.get(imageURL).content)


startTime = time()
waitPeriodInMinutes = 30

options = Options()
options.headless = False
chrome = webdriver.Chrome("./chromedriver", options = options)
chrome.implicitly_wait(5)

createDatasetDetailsCSV()

# while(True):
#     chrome.get("https://airnow.tehran.ir/")
#     closePopUpWindow(chrome)

#     imageURL = getImageURL(chrome)
#     saveImage(imageURL)
#     addDetailsToCSV(chrome)
#     print("Log: New Picture Scrapped At " + str(datetime.now()))
#     chrome.quit()
#     sleep( (waitPeriodInMinutes * 60.0) - ((time() - startTime) % (waitPeriodInMinutes * 60.0)) )

chrome.get("https://airnow.tehran.ir/")
closePopUpWindow(chrome)
retrieveAirQualityDetails(chrome)
chrome.quit()
