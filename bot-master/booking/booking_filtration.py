#includes instance methods
#will be responsible to interact with website
#after we have some results
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        
        
    def star_rating(self, minimum_stars):
        two = self.driver.find_element(By.CSS_SELECTOR, f'input[name="class=2"]')
        three = self.driver.find_element(By.CSS_SELECTOR, f'input[name="class=3"]')
        four = self.driver.find_element(By.CSS_SELECTOR, f'input[name="class=4"]')
        five = self.driver.find_element(By.CSS_SELECTOR, f'input[name="class=5"]')
        
        if(minimum_stars <= 2):
            self.driver.execute_script("arguments[0].click();", two)
        if(minimum_stars <= 3):
            self.driver.execute_script("arguments[0].click();", three)
        if(minimum_stars <= 4):
            self.driver.execute_script("arguments[0].click();", four)
        if(minimum_stars <= 5):
            self.driver.execute_script("arguments[0].click();", five)

    def price_filter(self):
            dropdown_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
            dropdown_button.click()
            time.sleep(2)

            wait = WebDriverWait(self.driver, 10)

            pricefilter = wait.until(EC.element_to_be_clickable(
                self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
            ))
            pricefilter.click()