import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class WhatsAppBot(threading.Thread):
    def __init__(self, phone_numbers, message, browser="chrome"):
        super().__init__()
        self.phone_numbers = phone_numbers
        self.message = message
        self.driver = None
        self.browser = browser.lower()

    def get_driver(self):
        if not self.driver:
            if self.browser == "chrome":
                options = webdriver.ChromeOptions()
                try:
                    self.driver = webdriver.Chrome(
                        executable_path=ChromeDriverManager().install(),
                        options=options,
                    )
                except WebDriverException as e:
                    if "Could not reach host" in str(e):
                        return "No internet connection"
            elif self.browser == "edge":
                options = webdriver.EdgeOptions()
                try:
                    self.driver = webdriver.Edge(
                        executable_path=EdgeChromiumDriverManager().install(),
                        options=options,
                    )
                except WebDriverException as e:
                    if "Could not reach host" in str(e):
                        return "No internet connection"
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")

        if self.driver is None:
            raise RuntimeError("Failed to create a WebDriver instance")

        self.driver.get("https://web.whatsapp.com/")
        return self.driver

    def search_contact(self, phone_number):
        try:
            search_box = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
                )
            )
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.RETURN)
        except TimeoutException:
            return "Element not found"

    def send_message(self):
        try:
            message_box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//div[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p',
                    )
                )
            )
            time.sleep(3)
            message_box.send_keys(self.message)
            time.sleep(3)
            message_box.send_keys(Keys.RETURN)
        except NoSuchElementException:
            return "Element not found"

    def run(self):
        driver = self.get_driver()
        if driver == "No internet connection":
            return "No internet connection"
        time.sleep(7)
        for phone_number in self.phone_numbers:
            search_result = self.search_contact(phone_number)
            if search_result == "Element not found":
                phone_number = phone_number[0:]
                wa_link = f"https://web.whatsapp.com/send/?phone=%{phone_number}&text&type=phone_number&app_absent=0"
                self.driver.get(wa_link)
                time.sleep(3)
            send_result = self.send_message()
            if send_result == "Element not found":
                continue
            time.sleep(2)
        self.driver.quit()
