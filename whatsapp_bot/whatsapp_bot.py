from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading




class WhatsAppBot(threading.Thread):    
    def __init__(self, phone_numbers, message):
        threading.Thread.__init__(self)
        self.phone_numbers = phone_numbers
        self.message = message
        self.driver = None

    
    def get_driver(self):
        if self.driver:
            return self.driver
        
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=chrome-data")
        options.add_argument("--profile-directory=Default")
        # Create a new instance of the web driver
        try:
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
            self.driver.get("https://web.whatsapp.com/")
        except WebDriverException as e:
            if "no such session" in str(e):
                return "No internet connection"
        return self.driver
    
    def search(self, driver, phone_number):
        try:
            search_box = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p'))
            )
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.RETURN)
            return None
        except TimeoutException:
            return "Timed out waiting for search box element to appear"
        
    def send_message(self, driver):
        try:
            message_box = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
                        )
            message_box.send_keys(self.message)
            message_box.send_keys(Keys.RETURN)
            return None
        except NoSuchElementException:
            return "Element not found"

    def run(self):
        # Go to the whatsapp web
        driver = self.get_driver()

        #wait for chat to load
        time.sleep(7)
        for phone_number in self.phone_numbers:
            # Find contact in search box
            self.search(driver,phone_number)
            #wait for chat to load
            time.sleep(3)
            #Enter message in message box
            try:
                self.send_message(driver)
            except TimeoutException:
                # Phone number is not saved as a contact, use wa.me link to send message
                phone_number = phone_number[0:]
                wa_link = f"https://web.whatsapp.com/send/?phone=%{phone_number}&text&type=phone_number&app_absent=0"
                driver.get(wa_link)
                self.send_message(driver)
            #wait for message to be sent
            time.sleep(2)

        #close the web driver
        driver.quit()