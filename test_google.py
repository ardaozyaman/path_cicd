import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

testv165 = "Google Search Testsshkjgkh"

def take_screenshot(driver, name):
    os.makedirs('reports/screenshots', exist_ok=True)
    path = f"reports/screenshots/{name}.png"
    driver.save_screenshot(path)
    return path

@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.binary_location = '/usr/bin/chromium'

    # Use system chromedriver instead of webdriver-manager
    chromedriver_paths = ['/usr/lib/chromium/chromedriver', '/usr/bin/chromedriver']
    chromedriver = None
    for path in chromedriver_paths:
        if os.path.exists(path):
            chromedriver = path
            break
    if not chromedriver:
        raise RuntimeError('chromedriver not found in system paths!')
    driver = webdriver.Chrome(service=Service(chromedriver), options=options)
    yield driver
    driver.quit()

def test_google_search_success(driver):

    driver.get("https://www.google.com")
    box = driver.find_element(By.NAME, "q")
    box.send_keys("Selenium Python")
    box.submit()
    time.sleep(2)
    assert "Selenium" in driver.title
    take_screenshot(driver, "success")

def test_google_search_fail(driver):
    driver.get("https://www.google.com")
    box = driver.find_element(By.NAME, "q")
    box.send_keys("asdasdasd1234567890")
    box.submit()
    time.sleep(2)
    try:
        assert "No results found" in driver.page_source
    except AssertionError:
        take_screenshot(driver, "fail")
        raise
