from selenium import webdriver
import booking.constants as const
from selenium.webdriver.common.by import By
import time

class Booking(webdriver.Chrome):
    def __init__(self, keep_open: bool = False, implicitly_wait: int = 10):
        self.keep_open = keep_open
        super().__init__()
        self.implicitly_wait(implicitly_wait)
        self.maximize_window()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency: str = "USD"):
        # Click on the currency button to open the dropdown
        self.find_element(By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']").click()
        
        # Select the currency using a simple XPath that looks for the currency text
        self.find_element(By.XPATH, f"//div[contains(text(), '{currency}')]").click()

    def select_place_to_go(self, place_to_go: str):
        self.find_element(By.XPATH, "//input[@name='ss']").send_keys(place_to_go)
        time.sleep(1)
        self.find_element(By.XPATH, f"//li[@id='autocomplete-result-{0}']").click()

    def select_date(self, check_in: str, check_out: str):
        """
        This function selects the check-in and check-out dates.
        Date format: YYYY-MM-DD
        """
        self.find_element(By.XPATH, f"//span[@data-date='{check_in}']").click()
        self.find_element(By.XPATH, f"//span[@data-date='{check_out}']").click()
    
    def select_adults(self, count: int = 1):
        """
        Select the number of adults for booking
        
        Args:
            count (int): Number of adults (1-30)
        """
        # First click on the occupancy config button to open the dropdown
        self.find_element(By.CSS_SELECTOR, "button[data-testid='occupancy-config']").click()
        
        # Get the current value
        adults_input = self.find_element(By.ID, "group_adults")
        current_value = int(adults_input.get_attribute("value"))
        
        # Find the container div that holds the buttons
        controls_container = self.find_element(By.XPATH, "//div[contains(@class, 'bfb38641b0')]")
        
        # Get all buttons in this container - the first is minus, the second is plus
        buttons = controls_container.find_elements(By.TAG_NAME, "button")
        minus_button = buttons[0]
        plus_button = buttons[1]
        
        while current_value:
            minus_button.click()
            current_value -= 1

        for _ in range(count - 1):
            plus_button.click()

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.keep_open:
            self.quit()
