import sys
import time
import os
from datetime import date

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from config import WhatsappConfig
from models import (get_db_session, WhatsappUserData, WhatsappMessageTable,)
from utils import (random_sleep, WhatsappVariables, whatsapp_login, validate_daily_limit, find_element_with_timeout,)


if __name__ == "__main__":
    engine = get_db_session(get_engine=True)
    session = get_db_session()
    whatsapp_variables = WhatsappVariables()

    if not validate_daily_limit(session):
        sys.exit()

    users = (session.query(WhatsappUserData).filter(WhatsappUserData.status == whatsapp_variables.not_sent_status)
             .order_by(WhatsappUserData.id).all())
    whatsapp_message = session.query(WhatsappMessageTable).first()

    if not whatsapp_message:
        print("Seems like message table is empty, please add a message what needs to be sent..")
        sys.exit()

    if not users:
        print("There are no users in the database with status 'Not Sent'. please add the user data and try again.")

    driver = whatsapp_login()
    if not driver:
        sys.exit()

    for user in users:
        try:
            if not validate_daily_limit(session, False):
                sys.exit()

            print(f"Sending message to {user.phone}")
            print(WhatsappConfig.WA_WEB_SEND_API.format(str(user.phone)))
            driver.get(WhatsappConfig.WA_WEB_SEND_API.format(str(user.phone)))
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass
            random_sleep()

            is_element_visible = None
            for _ in range(3):
                is_element_visible = find_element_with_timeout(driver, By.XPATH, whatsapp_variables.type_here_box,
                                                               timeout=5)

                if find_element_with_timeout(driver, By.XPATH, whatsapp_variables.invalid_phone_number_msg, timeout=5):
                    raise Exception(f"Invalid Phone number {user.phone}")

            if not is_element_visible:
                print("Unable to find the chat window, skipping this record.")
                continue

            random_sleep()
            chat_box = driver.find_element(By.XPATH, whatsapp_variables.type_here_box)
            chat_box.click()
            random_sleep()
            for msg in whatsapp_message.message.split(whatsapp_variables.new_line_delimiter):
                chat_box.send_keys(msg.strip())
                time.sleep(0.5)
                chat_box.send_keys(Keys.ALT + Keys.ENTER)

            random_sleep()
            if whatsapp_message.attachment:
                print("Attaching the attachment in message..")
                driver.find_element(By.XPATH, whatsapp_variables.attachment_box_xpath).click()
                random_sleep()
                file_name, file_extension = os.path.splitext(whatsapp_message.attachment)
                if file_extension in whatsapp_variables.allowed_file_ext:
                    image_box = driver.find_element(By.XPATH, whatsapp_variables.img_box_xpath1)
                    image_box.send_keys(whatsapp_message.attachment)
                else:
                    image_box = driver.find_element(By.XPATH, whatsapp_variables.img_box_xpath2)
                    image_box.send_keys(whatsapp_message.attachment)

            random_sleep()
            send_key = driver.find_element(By.XPATH, whatsapp_variables.send_msg_xpath)
            send_key.click()

            user.status = whatsapp_variables.sent_status
            user.updated_at = date.today().strftime('%Y-%m-%d')
            session.commit()
            random_sleep(5, 10)
            print(f"Message sent to {user.phone}")
        except Exception as e:
            print(f"Invalid Phone number {user.phone}")
            user.status = whatsapp_variables.invalid_status
            user.updated_at = date.today().strftime('%Y-%m-%d')
            session.commit()
