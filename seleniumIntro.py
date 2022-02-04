from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from datetime import datetime
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
    photoPath = f'./Photos/{str(datetime.now()).replace(":" , ",")}.jpg'

    with open(photoPath , 'wb') as handler:
        handler.write(requests.get(imageURL).content)



options = Options()
options.headless = False
chrome = webdriver.Chrome(".\chromedriver", options = options)

chrome.implicitly_wait(5)
chrome.get("https://airnow.tehran.ir/")

closePopUpWindow(chrome)
imageURL = getImageURL(chrome)
saveImage(imageURL)

chrome.quit()