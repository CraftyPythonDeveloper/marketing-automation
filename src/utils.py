import time
from dataclasses import dataclass, field
from datetime import date
import random

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from models import WhatsappUserData
from config import WhatsappConfig


@dataclass
class WhatsappVariables:
    verify_login_xpath: str = '//h1[text()="Chats"]'
    type_here_box: str = "//div[@aria-label='Type a message']"
    send_msg_xpath: str = "//span[@data-testid='send' or @data-icon='send']"
    new_line_delimiter: str = "<br>"
    attachment_box_xpath: str = "//div[@aria-label='Attach']"
    img_box_xpath1: str = "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
    img_box_xpath2: str = "//input[@accept='*']"
    invalid_phone_number_msg: str = "//div[text()='Phone number shared via url is invalid.']"
    allowed_file_ext: list = field(default_factory=lambda: [".png", ".jpeg", ".jpg", ".gif", ".jfif", ".mp4", ".3gp"])
    not_sent_status = "Not Sent"
    sent_status = "Sent"
    invalid_status = "Invalid"


def random_sleep(min_time: float = 1, max_time: float = 5) -> bool:
    time.sleep(random.uniform(min_time, max_time))
    return True


def find_element_with_timeout(driver, by, locator, timeout=120):
    for _ in range(timeout):
        try:
            driver.find_element(by, locator)
            return True
        except:
            time.sleep(1)

    return False


def whatsapp_login():
    profile_path = r"C:\Users\Anon\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default"
    wa_variables = WhatsappVariables()
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--user-data-dir=' + profile_path)
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = Chrome(options=chrome_options)
    driver.get(WhatsappConfig.WA_WEB_URL)
    print("Please scan the QR code to login into whatsapp web.")

    login_status = find_element_with_timeout(driver, By.XPATH, wa_variables.verify_login_xpath, 180)
    if not login_status:
        print("Login process timeout, please try again..")
        return False

    random_sleep(5, 10)
    print("Thankyou for logging in, script will now automatically continue.")
    return driver


def validate_daily_limit(session, log=True):
    today_count = session.query(WhatsappUserData).filter(WhatsappUserData.updated_at == date.today().strftime('%Y-%m-%d'),
                                                         WhatsappUserData.status == "Sent").count()
    if today_count > WhatsappConfig.WA_DAILY_LIMIT:
        print(f"You have already sent {today_count} messages today. Please continue tomorrow to avoid getting blocked")
        return False
    if log:
        print(f"You have sent {today_count} messages today.")
    return True

