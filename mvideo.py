from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def initializer(url):
    """
    func launches firefox browser with geckodriver
    """
    (*RESOLUTION,) = 1920, 1080

    service = Service("./geckodriver")
    browser = webdriver.Firefox(service=service)
    browser.set_window_size(*RESOLUTION)
    browser.get(url)
    return browser


def target_handler(browser, target):
    """
    func tries to find span with target text
    """
    try:
        link = browser.find_element(By.XPATH, f"//span[contains(text(),'{target}')]")
    except NoSuchElementException:
        link = None
    return link


def scroller(browser, target):
    """
    func scrolls web-page until finds span with target text
    """
    actions = ActionChains(browser)
    link = target_handler(browser, target)
    while not link:
        actions.scroll_by_amount(0, 500).perform()
        link = target_handler(browser, target)
    return link


url = "https://www.mvideo.ru/"
browser = initializer(url)
button = scroller(browser, target="В тренде")
button.click()
arrow_button = browser.find_elements(By.XPATH, '//mvid-shelf-group//button[contains(@class, "btn forward")]')[-1]
arrow_button.click()
print()
browser.quit()
