from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

options = Options()
options.headless = True
chrome = webdriver.Chrome(".\chromedriver", options = options)

chrome.implicitly_wait(10)
chrome.get("https://airnow.tehran.ir/")

imageURL = chrome.find_element(
    By.ID, "imgHeader"
).get_attribute(
    "src"
)

photoPath = f'.\Photos\{str(datetime.now()).replace(":" , ",")}.jpg'

with open(photoPath , 'wb') as handler:
    handler.write(requests.get(imageURL).content)

chrome.quit()