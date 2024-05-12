class DatabaseConfig:
    DB_CONNECTION_URI = "sqlite:///marketing.db"

    # MS SQL connection string
    # SERVER_NAME = "localhost"
    # DATABASE_NAME = ""
    # DRIVER_NAME = ""
    # DB_CONNECTION_URI = f'mssql+pyodbc://{SERVER}/{DATABASE}?driver={DRIVER}'


class WhatsappConfig(DatabaseConfig):
    WA_DAILY_LIMIT = 450
    WA_WEB_URL = 'https://web.whatsapp.com'
    WA_WEB_SEND_API = 'https://web.whatsapp.com/send?phone=+91{0}'


class EmailConfig(DatabaseConfig):
    pass
