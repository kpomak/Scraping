from selenium import webdriver
from selenium.webdriver.firefox.service import Service


service = Service("./geckodriver")
browser = webdriver.Firefox(service=service)
browser.get("https://mvideo.ru/")

browser.quit()
