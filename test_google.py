import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

class InsiderCareersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.binary_location = '/usr/bin/chromium'
        chromedriver_paths = ['/usr/lib/chromium/chromedriver', '/usr/bin/chromedriver']
        chromedriver = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                chromedriver = path
                break
        if not chromedriver:
            raise RuntimeError('chromedriver not found in system paths!')
        cls.driver = webdriver.Chrome(service=Service(chromedriver), options=options)
        os.makedirs('reports/screenshots', exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_find_dream_job_button(self):
        self.driver.get("https://useinsider.com/careers")
        time.sleep(3)
        # Kontrol edilecek elementin varlığı
        elements = self.driver.find_elements(By.XPATH, '//a[@href="https://useinsider.com/open-positions/" and contains(@class, "btn-info") and contains(@class, "rounded") and contains(@class, "py-3")]')
        self.driver.save_screenshot('reports/screenshots/find_dream_job.png')
        self.assertTrue(len(elements) > 0, 'Find your dream job butonu bulunamadı!')

if __name__ == "__main__":
    unittest.main()
