class DatabaseConfig:
    DB_CONNECTION_URI = "sqlite:///marketing.db"

    # MS SQL connection string
    # SERVER_NAME = "localhost"
    # DATABASE_NAME = ""
    # DRIVER_NAME = ""
    # DB_CONNECTION_URI = f'mssql+pyodbc://{SERVER}/{DATABASE}?driver={DRIVER}'


class WhatsappConfig(DatabaseConfig):
    WA_WEB_URL = 'https://web.whatsapp.com'
    WA_WEB_SEND_API = 'https://web.whatsapp.com/send?phone=+91{0}'
    CHROME_PROFILE_NAME = "wa_profile1"

    # User config, please update it as per your requirements.
    WA_DAILY_LIMIT = 450
    WHATSAPP_MESSAGE = "This is a test message"
    WHATSAPP_ATTACHMENT = r"C:\Users\Anon\Downloads\test.png"  # only replace the path, DO NOT REMOVE r"
    # WHATSAPP_ATTACHMENT = None    # if you don't want attachment, then you can keep this None


class EmailConfig(DatabaseConfig):
    HOST = ""
    SMTP_PORT = 465
    SMTP_EMAIL = ""
    SMTP_PASSWORD = ""

    # User config, please update it as per your requirements.
    EMAIL_DAILY_LIMIT = 100

    # generate email templates from any of below website
    # 1. https://wordtohtml.net/site/index
    # 2. https://www.textfixer.com/html/convert-email-to-html.php
    # 3. https://www.tiny.cloud/
    EMAIL_TEMPLATE_NAME = "test_email_template.html"
    SUBJECT = "This is test email"
    ATTACHMENT_PATH = r"C:\Users\Anon\Downloads\test.png"    # Only replace the path, DO NOT REMOVE r"
    # WHATSAPP_ATTACHMENT = None    # if you don't want attachment, then you can keep this None
