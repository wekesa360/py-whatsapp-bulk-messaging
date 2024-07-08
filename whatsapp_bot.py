import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import urllib.parse
import time
import os
import stat
from constants import (
    MAX_RETRY_ATTEMPTS,
    CHAT_LOAD_TIMEOUT,
)


class WhatsAppBot:
    def __init__(self, browser_name, log_callback, headless=False):
        self.driver = None
        self.browser_name = browser_name
        self.user_data_dir = os.path.join(tempfile.gettempdir(), "whatsapp_user_data")
        self.log_callback = log_callback
        self.stop_flag = False
        self.headless = headless
        self.ensure_user_data_dir()

    def ensure_user_data_dir(self):
        try:
            if not os.path.exists(self.user_data_dir):
                os.makedirs(self.user_data_dir)
                if os.name == "nt":  # Windows
                    import win32api
                    import win32security
                    user_sid = win32security.LookupAccountName(None, win32api.GetUserName())[0]
                    security_descriptor = win32security.GetFileSecurity(self.user_data_dir, win32security.DACL_SECURITY_INFORMATION)
                    dacl = win32security.ACL()
                    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32security.FILE_ALL_ACCESS, user_sid)
                    security_descriptor.SetSecurityDescriptorDacl(1, dacl, 0)
                    win32security.SetFileSecurity(self.user_data_dir, win32security.DACL_SECURITY_INFORMATION, security_descriptor)
                else:  # Unix-based systems and Linux
                    os.chmod(self.user_data_dir, stat.S_IRWXU)
        except Exception as e:
            raise Exception(f"Failed to create user data directory: {str(e)}")

    def initialize_driver(self):
        if not self.driver:
            try:
                if self.browser_name == "Chrome":
                    service = ChromeService(ChromeDriverManager().install())
                    options = webdriver.ChromeOptions()
                    options.add_argument(f"user-data-dir={self.user_data_dir}")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-extensions")
                    options.add_argument("--disable-logging")
                    options.add_argument("--log-level=3")
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    if self.headless:
                        options.add_argument("--headless")
                    self.driver = webdriver.Chrome(service=service, options=options)
                elif self.browser_name == "Firefox":
                    service = FirefoxService(GeckoDriverManager().install())
                    options = webdriver.FirefoxOptions()
                    options.add_argument(f"-profile {self.user_data_dir}")
                    if self.headless:
                        options.add_argument("-headless")
                    self.driver = webdriver.Firefox(service=service, options=options)
                elif self.browser_name == "Edge":
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    options = webdriver.EdgeOptions()
                    options.add_argument(f"user-data-dir={self.user_data_dir}")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--disable-extensions")
                    options.add_argument("--disable-logging")
                    options.add_argument("--log-level=3")
                    if self.headless:
                        options.add_argument("--headless")
                    self.driver = webdriver.Edge(service=service, options=options)
                else:
                    raise ValueError(f"Unsupported browser: {self.browser_name}")

                self.driver.get("https://web.whatsapp.com/")
                self.wait_for_login()
            except WebDriverException as e:
                raise Exception(f"Failed to initialize the browser: {str(e)}")

    def wait_for_login(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="side"] | //canvas[@aria-label="Scan me!"]'))
            )
            
            if self.driver.find_elements(By.XPATH, '//div[@id="side"]'):
                self.log_callback("Already logged in!")
            else:
                self.log_callback("Please scan the QR code to log in.")
                WebDriverWait(self.driver, 300).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="side"]'))
                )
                self.log_callback("Successfully logged in!")
        except TimeoutException:
            raise Exception("Failed to log in to WhatsApp Web. Please try again.")

    def dismiss_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        except:
            return None

    def send_message(self, phone_number, message):
        attempts = 0
        while attempts < MAX_RETRY_ATTEMPTS and not self.stop_flag:
            try:
                encoded_phone = urllib.parse.quote(phone_number)
                encoded_message = urllib.parse.quote(message)
                
                chat_url = f"https://web.whatsapp.com/send/?phone={encoded_phone}&text={encoded_message}"
                
                self.driver.get(chat_url)
                
                alert_text = self.dismiss_alert()
                if alert_text:
                    self.log_callback(f"Alert dismissed: {alert_text}")
                
                try:
                    send_button = WebDriverWait(self.driver, CHAT_LOAD_TIMEOUT).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
                    )
                except TimeoutException:
                    raise Exception("Chat interface did not load. The number might not be on WhatsApp.")
                
                send_button.click()
                time.sleep(2)
                
                alert_text = self.dismiss_alert()
                if alert_text:
                    self.log_callback(f"Alert dismissed after sending: {alert_text}")
                
                self.log_callback(f"Message sent successfully to {phone_number}")
                return True
            except Exception as e:
                attempts += 1
                self.log_callback(f"Attempt {attempts} failed for {phone_number}: {str(e)}")
                if attempts == MAX_RETRY_ATTEMPTS:
                    self.log_callback(f"Failed to send message to {phone_number} after {MAX_RETRY_ATTEMPTS} attempts")
                    return False
                time.sleep(2)  # Wait before retrying
        return False

    def close(self):
        if self.driver:
            self.driver.quit()
