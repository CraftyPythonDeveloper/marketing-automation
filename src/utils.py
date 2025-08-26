import os
from pathlib import Path
import time
from dataclasses import dataclass, field
from datetime import date
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from undetected_chromedriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

from config import WhatsappConfig, EmailConfig


WRK_DIR = Path(__file__).parent


@dataclass
class WhatsappVariables:
    verify_login_xpath: str = '//div[text()="Unread"]'
    type_here_box: str = "//div[@aria-label='Type a message'] | //div[@aria-placeholder='Type a message']"
    send_msg_xpath: str = "//span[@data-testid='send' or @data-icon='send'] | //div[@aria-label='Send']"
    new_line_delimiter: str = "<br>"
    attachment_box_xpath1: str = "//div[@aria-label='Attach']"
    attachment_box_xpath2: str = "//button[@title='Attach']"
    img_box_xpath1: str = "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
    img_box_xpath2: str = "//input[@accept='*']"
    invalid_phone_number_msg: str = "//div[text()='Phone number shared via url is invalid.']"
    allowed_file_ext: list = field(default_factory=lambda: [".png", ".jpeg", ".jpg", ".gif", ".jfif", ".mp4", ".3gp"])
    not_sent_status: str = "Not Sent"
    sent_status: str = "Sent"
    invalid_status: str = "Invalid"


@dataclass
class EmailVariables:
    not_sent_status: str = "Not Sent"
    sent_status: str = "Sent"
    invalid_status: str = "Invalid"


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
    profile_path = os.path.join(WRK_DIR, "chrome_profiles", WhatsappConfig.CHROME_PROFILE_NAME)
    wa_variables = WhatsappVariables()
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--user-data-dir=' + profile_path)
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(WhatsappConfig.WA_WEB_URL)
    print("Please scan the QR code to login into whatsapp web.")

    login_status = find_element_with_timeout(driver, By.XPATH, wa_variables.verify_login_xpath, 180)
    if not login_status:
        print("Login process timeout, please try again..")
        return False

    random_sleep(5, 10)
    print("Thankyou for logging in, script will now automatically continue.")
    return driver


def paste_content(driver, el, content):
    # https://stackoverflow.com/questions/51706256/sending-emojis-with-seleniums-send-keys
    driver.execute_script(
      f'''
        const text = `{content}`;
        const dataTransfer = new DataTransfer();
        dataTransfer.setData('text', text);
        const event = new ClipboardEvent('paste', {{
          clipboardData: dataTransfer,
          bubbles: true
        }});
        arguments[0].dispatchEvent(event)
    ''', el)
    return True


def validate_daily_limit(session, model, status, daily_limit, log=True):
    today_count = session.query(model).filter(model.updated_at == date.today().strftime('%Y-%m-%d'),
                                              model.status == status).count()

    if today_count >= daily_limit:
        print(f"Set limit of {daily_limit} exceeded. Please try again tomorrow")
        return False
    if log:
        print(f"You have sent {today_count} messages today.")
    return True


def login_email():
    smtp_server = smtplib.SMTP_SSL(EmailConfig.HOST, EmailConfig.SMTP_PORT)
    smtp_server.login(EmailConfig.SMTP_EMAIL, EmailConfig.SMTP_PASSWORD)
    return smtp_server


def send_email(smtp_server, to):
    msg = MIMEMultipart()
    msg['From'] = EmailConfig.SMTP_EMAIL
    msg['To'] = to
    msg['Subject'] = EmailConfig.SUBJECT

    template_path = os.path.join(WRK_DIR, "email_templates", EmailConfig.EMAIL_TEMPLATE_NAME)
    with open(template_path, "r", encoding="UTF-8") as fp:
        email_body = fp.read()

    html_content = MIMEText(email_body, 'html')
    msg.attach(html_content)

    if EmailConfig.ATTACHMENT_PATH:
        for attachment in EmailConfig.ATTACHMENT_PATH.split(";"):
            with open(attachment, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {attachment}")
            msg.attach(part)

    smtp_server.send_message(msg)
    return True
