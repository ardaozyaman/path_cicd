import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

testv1 = "Google Search Tests"

def take_screenshot(driver, name):
    os.makedirs('reports/screenshots', exist_ok=True)
    path = f"reports/screenshots/{name}.png"
    driver.save_screenshot(path)
    return path

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
