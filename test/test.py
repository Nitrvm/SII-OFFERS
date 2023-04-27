from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


driver = webdriver.Chrome("chromedriver.exe")
driver.get(os.getcwd()+'code.html')

