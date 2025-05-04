import os
import booking.constants as const
import time

from booking.booking_filtration import BookingFiltration

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        # Open currency picker
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        # Wait and click on USD
        wait = WebDriverWait(self, 10)
        currency_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(text(), '{currency}')]/ancestor::button")
        ))
        currency_button.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.NAME, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(2)

        wait = WebDriverWait(self, 10)

        wait.until(EC.visibility_of_element_located(
            (By.ID, "autocomplete-results")
        ))
        self.implicitly_wait(10)
        auto_result = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
        ))
        auto_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        check_in_element.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        check_out_element.click()

    def travellers(self, adults):
        dropdown = self.find_element(By.CSS_SELECTOR, 'span[data-testid="searchbox-form-button-icon"]')
        dropdown.click()
        adult_clear = self.find_element(By.CSS_SELECTOR, 'button[class="de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 c857f39cb2"]')
        adult_clear.click()
        adult_add = self.find_element(By.CSS_SELECTOR, 'button[class="de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 dc8366caa6"]')
        count = 1

        while(count < adults):
            adult_add.click()
            count = count + 1

    def submit(self):
        submit_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()


    def apply_filtrations(self):
        time.sleep(2)
        filtration = BookingFiltration(driver=self)
        filtration.star_rating(minimum_stars=3)
        filtration.price_filter()

    def report_results(self):
        wait = WebDriverWait(self, 5)

        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, '[data-testid="property-card"]'
            )))
    
        property_cards = self.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')
    
        first_15 = property_cards[:15]

        for index, card in enumerate(first_15, start=1):
            try:
                title = card.find_element(By.CSS_SELECTOR, '[data-testid="title"]').text
                link = card.find_element(By.CSS_SELECTOR, '[data-testid="title-link"]').get_attribute('href')
                price = card.find_element(By.CSS_SELECTOR, '[data-testid="price-and-discounted-price"]').text
                print(f"\n{index}. {title} -> Price: {price}\n{link}\n")
            except Exception as e:
                print(f"Error extracting info from card {index}: {e}")


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

