from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from booking.booking import Booking

def click_button_and_wait(driver: webdriver):
    # Go to the website
    driver.get('https://the-internet.herokuapp.com/dynamic_loading/2')
    
    # Find the button - this is the key part!
    # The button is inside the div with id="start"
    button = driver.find_element(By.CSS_SELECTOR, "button")
    print("Found the button!")
    
    # Click the button
    button.click()
    print("Clicked the button!")
    
    # Wait for the result to appear
    wait = WebDriverWait(driver, 10)
    result = wait.until(EC.visibility_of_element_located((By.ID, "finish")))
    
    # Print what we found
    print(f"Result text: {result.text}")

def form_filling(driver: webdriver):
    driver.get('https://the-internet.herokuapp.com/login')
    driver.find_element(By.ID, 'username').send_keys('tomsmith')
    driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
    driver.find_element(By.CSS_SELECTOR, "button").click()

def basic_functions():
    # Create a Chrome driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    """
        Basic Functions:
        1. Click the button and wait for the result to appear
        2. Fill in the form and submit

    """
    click_button_and_wait(driver)
    form_filling(driver)
    
    # Wait a moment so we can see the result
    time.sleep(3)
    
    # Close the browser
    driver.quit()


def main():
    with Booking(keep_open=True) as booking:
        booking.land_first_page()
        booking.change_currency(currency="USD")
        booking.select_place_to_go("New York")
        booking.select_date("2025-03-09", "2025-03-15")
        booking.select_adults(5)
        input("Press Enter to close the browser...")
        # time.sleep(5)
    return 0

if __name__ == "__main__":
    main()
