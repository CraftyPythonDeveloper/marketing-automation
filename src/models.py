import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, func, inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DatabaseConfig


# database model
base = declarative_base()


class WhatsappUserData(base):
    __tablename__ = "whatsapp_user_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), server_default="Not Sent", nullable=False)
    created_at = db.Column(DateTime, server_default=func.now())
    updated_at = db.Column(db.String(50), nullable=True)


class WhatsappMessageTable(base):
    __tablename__ = "whatsapp_message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.String(50), nullable=True)


class EmailUserData(base):
    __tablename__ = "email_user_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    status = db.Column(db.String(50), server_default="Not Sent", nullable=False)
    created_at = db.Column(DateTime, server_default=func.now())
    updated_at = db.Column(db.String(50), nullable=True)


class EmailMessageTable(base):
    __tablename__ = "email_message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(500), nullable=True)
    created_at = db.Column(DateTime, server_default=func.now())
    updated_at = db.Column(db.String(50), nullable=True)


def get_db_session(get_engine=False):
    engine = create_engine(DatabaseConfig.DB_CONNECTION_URI)

    try:
        engine.connect()
    except:
        print("Unable to connect to database, please check your database connection uri")

    if get_engine:
        return engine

    return sessionmaker(bind=engine)()


engine = get_db_session(get_engine=True)
if not inspect(engine).has_table("whatsapp_user_data"):
    # If tables don't exist, create them
    base.metadata.create_all(engine)
    print("Created all the tables..")
