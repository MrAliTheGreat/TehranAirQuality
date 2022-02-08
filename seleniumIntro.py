from tkinter import Button
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from datetime import datetime
from time import time, sleep
import requests
import pandas



def createDatasetDetailsCSV():
    try:
        datasetDetailsFile = open("./DatasetDetails.csv")
        datasetDetailsFile.close()
    except FileNotFoundError:
        pandas.DataFrame(
            columns = ["File Name", "Date", "Time", "Current AQI", "Past 24h AQI", "Current Main Pollutant", "Past 24h Main Pollutant",
                        "CO", "O3", "SO2", "NO2", "PM2.5", "PM10",
                        "Current Temperature", "Weather Status", "Wind Speed",
                        "Relative Humidity", "Horizontal Visibility", "Rainfall Amount Past 24h"]
        ).to_csv("./DatasetDetails.csv" , index = False, header = True)

def getParticleAmount(parentDivID, divID):
    return chrome.find_element(
        By.ID, parentDivID
    ).find_element(
        By.ID, divID
    ).get_attribute("innerHTML")

def retrievePollutantDetails(chrome : WebDriver):
    chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblMoreInfo1"
    ).click()

    CO_amount = getParticleAmount(
        parentDivID = "ContentPlaceHolder1_trCO",
        divID = "ContentPlaceHolder1_OnlineDetailCO_lblCurrent"
    )
    O3_amount = getParticleAmount(
        parentDivID = "ContentPlaceHolder1_trO3",
        divID = "ContentPlaceHolder1_OnlineDetailO3_lblCurrent"
    )
    SO2_amount = getParticleAmount(
        parentDivID = "ContentPlaceHolder1_trSO2",
        divID = "ContentPlaceHolder1_OnlineDetailSO2_lblCurrent"
    )
    NO2_amount = getParticleAmount(
        parentDivID = "ContentPlaceHolder1_trNO2",
        divID = "ContentPlaceHolder1_OnlineDetailNO2_lblCurrent"
    )
    PM2_5_amount = getParticleAmount(
        parentDivID = "ContentPlaceHolder1_trPM2_5",
        divID = "ContentPlaceHolder1_OnlineDetailPM2_5_lblCurrent"
    )
    PM10_amount = getParticleAmount(
        parentDivID = "ContentPlaceHolder1_trPM10",
        divID = "ContentPlaceHolder1_OnlineDetailPM10_lblCurrent"
    )

    return CO_amount, O3_amount, SO2_amount, NO2_amount, PM2_5_amount, PM10_amount

def retrieveAirQualityDetails(chrome : WebDriver):
    airQualityIndexNow = chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblAqi3h"
    ).get_attribute("innerHTML")

    airQualityIndexPast24h = chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblAqi24h"
    ).get_attribute("innerHTML")

    mainPollutantNow = str(chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblAqi3hDesc"
    ).get_attribute("innerHTML")).split(":")[1].strip()

    mainPollutantPast24h = str(chrome.find_element(
        By.ID, "ContentPlaceHolder1_lblAqi24hDesc"
    ).get_attribute("innerHTML")).split(":")[1].strip()

    return airQualityIndexNow, airQualityIndexPast24h, mainPollutantNow, mainPollutantPast24h

def retrieveWeatherDetails(chrome : WebDriver):
    chrome.get("https://www.irimo.ir/eng/index.php?module=web_directory&wd_id=701&id=17561&ctitle=Weather%20Forcast%20Tehran")
    weatherInfo = chrome.find_element(
        By.ID, "divCurrentWeather"
    )
    
    currentTemperature = weatherInfo.find_element(
        By.CSS_SELECTOR, 'div[style="font-size:48px;direction:ltr"]'
    ).get_attribute("innerHTML")[:-3]

    weatherStatus = weatherInfo.find_element(
        By.CSS_SELECTOR, 'div[style="font-size:18px;"]'
    ).get_attribute("innerHTML")

    OtherDetails = weatherInfo.find_elements(
        By.CSS_SELECTOR, 'span[class="wet_s_wblk_data"]'
    )

    windSpeed = str(OtherDetails[0].get_attribute("innerHTML")).split("m/s")[0]
    relativeHumidity = OtherDetails[1].get_attribute("innerHTML")
    horizontalVisibility = OtherDetails[2].get_attribute("innerHTML")
    rainfallPast24h = OtherDetails[3].get_attribute("innerHTML")

    return currentTemperature, weatherStatus, windSpeed, relativeHumidity, horizontalVisibility, rainfallPast24h




def addDetailsToCSV(chrome : WebDriver):
    lastFileName = len(pandas.read_csv("./DatasetDetails.csv"))
    date, time = str(datetime.now()).split()
    hour, minute, _ = time.split(":")

    AQI_Now, AQI_Past24h, mainPollutantNow, mainPollutantPast24h = retrieveAirQualityDetails(chrome)
    CO, O3, SO2, NO2, PM2_5, PM10 = retrievePollutantDetails(chrome)

    temperature, weatherStatus, windSpeed, relativeHumidity, visibility, rainfallPast24h = retrieveWeatherDetails(chrome)
    
    info = \
    {
        "File Name" : str(lastFileName + 1),
        "Date" : date,
        "Time" : ":".join([hour, minute]),
        "Current AQI" : AQI_Now,
        "Past 24h AQI" : AQI_Past24h,
        "Current Main Pollutant" : mainPollutantNow,
        "Past 24h Main Pollutant" : mainPollutantPast24h,
        "CO" : CO,
        "O3" : O3,
        "SO2" : SO2,
        "NO2" : NO2,
        "PM2.5" : PM2_5,
        "PM10" : PM10,
        "Current Temperature" : temperature,
        "Weather Status" : weatherStatus,
        "Wind Speed" : windSpeed,
        "Relative Humidity" : relativeHumidity,
        "Horizontal Visibility" : visibility,
        "Rainfall Amount Past 24h" : rainfallPast24h
    }

    pandas.DataFrame(info , index = [0]).to_csv("./DatasetDetails.csv", mode = "a", index = False, header = False)

def closePopUpWindow(chrome : WebDriver):
    closeButton = chrome.find_element(
        By.ID, "GuideMedical"
    ).find_element(
        By.CSS_SELECTOR , 'button[aria-label="Close"]'
    )

    if(closeButton.is_displayed()):
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
options.headless = True
chrome = webdriver.Chrome("./chromedriver", options = options)
chrome.implicitly_wait(5)

createDatasetDetailsCSV()

while(True):    
    chrome.get("https://airnow.tehran.ir/")
    closePopUpWindow(chrome)

    imageURL = getImageURL(chrome)
    saveImage(imageURL)
    addDetailsToCSV(chrome)
    print("Log: New Data Added At " + str(datetime.now()))
    sleep( (waitPeriodInMinutes * 60.0) - ((time() - startTime) % (waitPeriodInMinutes * 60.0)) )
