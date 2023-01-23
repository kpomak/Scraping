import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


PAUSE = 1  # time of sleep in sec
(*RESOLUTION,) = 1920, 1080  # resolution of browsers window
SCROLL_SPEED = 500  # quantity of scrolled pixels


def initializer(url: str) -> webdriver.Firefox:
    """
    func launches firefox browser with geckodriver
    """
    service = Service("./geckodriver")
    browser = webdriver.Firefox(service=service)
    browser.implicitly_wait(3)
    browser.set_window_size(*RESOLUTION)
    browser.get(url)
    return browser


def target_handler(
    browser: webdriver.Firefox, target: str
) -> webdriver.Firefox._web_element_cls:
    """
    func tries to find span with target text
    """
    try:
        link = browser.find_element(By.XPATH, f"//span[contains(text(),'{target}')]")
    except NoSuchElementException:
        link = None
    return link


def scroller(
    browser: webdriver.Firefox, target: str
) -> webdriver.Firefox._web_element_cls:
    """
    func scrolls web-page until finds span with target text
    """
    actions = ActionChains(browser)
    link = target_handler(browser, target)
    while not link:
        actions.scroll_by_amount(0, SCROLL_SPEED).perform()
        time.sleep(PAUSE)
        link = target_handler(browser, target)
    return link


def carousel_roll(browser: webdriver.Firefox) -> set:
    """
    func rolls the goods carousel and scraps goods info
    """
    pattern = '//mvid-shelf-group//button[contains(@class, "btn forward")]'
    goods_links = set()
    goods = []
    wait = WebDriverWait(browser, 10)
    next_button = wait.until(EC.presence_of_all_elements_located((By.XPATH, pattern)))
    while next_button:
        try:
            next_button[-1].click()
        except ElementNotInteractableException:
            break

        time.sleep(PAUSE)
        items = goodse_parse(browser)

        for item in items:  # check repeating  goods
            if item["link"] in goods_links:
                continue
            else:
                goods_links.add(item["link"])
                goods.append(item)

        next_button = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, pattern))
        )
    return goods


def goodse_parse(browser: webdriver.Firefox) -> list:
    """
    func parses web page according to patterns and returns list of dicts with goods info
    """
    product_card = browser.find_element(
        By.XPATH, "//mvid-shelf-group//mvid-product-cards-group"
    )

    links = product_card.find_elements(
        By.XPATH, ".//div[contains(@class, 'product-mini-card__name')]//a"
    )
    prices = product_card.find_elements(
        By.XPATH, ".//span[contains(@class, 'price__main-value')]"
    )

    return [
        {"name": link.text, "price": price.text, "link": link.get_attribute("href")}
        for link, price in zip(links, prices)
    ]


def db_save(goods: list) -> None:
    client = MongoClient("mongodb://root:pass@localhost:27017")
    db = client.mvideo
    collection = db.trands
    collection.insert_many(goods)


if __name__ == "__main__":
    url = "https://www.mvideo.ru/"
    browser = initializer(url)
    scroller(browser, target="В тренде").click()
    goods = carousel_roll(browser)
    db_save(goods)
    browser.quit()
