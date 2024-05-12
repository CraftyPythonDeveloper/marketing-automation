import sys
from datetime import date
from config import EmailConfig
from models import EmailUserData, get_db_session
from utils import validate_daily_limit, login_email, send_email, EmailVariables, random_sleep


if __name__ == '__main__':
    session = get_db_session()
    email_variables = EmailVariables()

    if not validate_daily_limit(session=session, model=EmailUserData, status=email_variables.sent_status,
                                daily_limit=EmailConfig.EMAIL_DAILY_LIMIT):
        sys.exit()

    users = (session.query(EmailUserData).filter(EmailUserData.status == email_variables.not_sent_status)
             .order_by(EmailUserData.id).all())

    if not users:
        print("There are no users in the database with status 'Not Sent'. please add the user data and try again.")
        sys.exit()

    try:
        smtp_server = login_email()
    except Exception as e:
        print("Unable to login to SMTP ", e)
        sys.exit()

    for user in users:
        try:
            send_email(smtp_server, user.email)

            user.status = email_variables.sent_status
            user.updated_at = date.today().strftime('%Y-%m-%d')
            session.commit()
            random_sleep()
            print(f"Message sent to {user.email}")
        except Exception as e:
            print(f"Invalid Phone number {user.email}")
            user.status = email_variables.invalid_status
            user.updated_at = date.today().strftime('%Y-%m-%d')
            session.commit()

    smtp_server.quit()
