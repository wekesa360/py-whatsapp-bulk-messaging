from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import os
import threading

class WhatsAppBot(threading.Thread):
    def __init__(self, phon_number, message):
        threading.Thread.__init__(self)
        self.phone_number = phon_number
        self.message = message
        self.driver = None
    
    def get_driver(self):
        # Check if a driver instance already exists
        if self.driver:
            return self.driver

        # Load the session from the file if it exists
        session_file_path = "whatsapp_session.pkl"
        try:
            with open(session_file_path, "rb") as f:
                session = pickle.load(f)
            self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
            self.driver.session_id = session["session_id"]
            self.driver.command_executor._url = session["executor_url"]
            return self.driver
        except FileNotFoundError:
            pass

        # If session file does not exist, create a new driver instance
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=chrome-data")
        options.add_argument("--profile-directory=Default")
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=options)
        self.driver.get("https://web.whatsapp.com/")
        
        # Save the session to a file
        session = {
            "session_id": self.driver.session_id,
            "executor_url": self.driver.command_executor._url,
        }
        with open(session_file_path, "wb") as f:
            pickle.dump(session, f)

        return self.driver

    def run(self):
        # Create a new instance of the web driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        # Go to the whatsapp web
        driver.get("https://web.whatsapp.com/")

        #wait for chat to load
        time.sleep(10)

        # Find contact in search box
        try:
            search_box = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p'))
            )
            search_box.send_keys(self.phone_number)
            search_box.send_keys(Keys.RETURN)
        except TimeoutException:
            return "Timed out waiting for search box element to appear"

        #wait for chat to load
        time.sleep(5)

        #Enter message in message box
        try:
            message_box = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
            )
            message_box.send_keys(self.message)
            message_box.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Timed out waiting for search box element to appear")

        #wait for message to be sent
        time.sleep(2)

        #close the web driver
        driver.quit()

if __name__ == "__main__":
    # Create a new instance of the whatsapp bot
    whatsapp_bot = WhatsAppBot(["+254792589417"], "Hello world")
    whatsapp_bot.start()
    whatsapp_bot.join()