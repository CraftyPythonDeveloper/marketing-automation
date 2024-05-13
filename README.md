# Marketing Automation

This repo is about automating running campaigns on social media platforms using **Python Selenium**.
<br><br> Below are currently supported social medias.
* Whatsapp - send cold messages to new numbers on whatsapp.
* Email - send cold/promotional emails to multiple users.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Installation

* Make sure python is installed and accessible through terminal/cmd by typing ```python --version``` or ```python3 --version```
* (Optional step) Create virtual environment by following tutorial on [How to install virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
* Clone the repo locally using ```git clone https://github.com/CraftyPythonDeveloper/marketing-automation.git```
* Install requirements ```pip install -r requirements.txt```

## Usage

To run the script follow the below mentioned steps:

### 1. Usage For Whatsapp Automation
- update the config.py.
  - Update the **DB_CONNECTION_URI** with your database details, an example to connect to MS SQL is already commented out
  - Then in WhatsappConfig class, update the config according to your requirements. Below are details about variables.
    - **CHROME_PROFILE_NAME** - (Optional) This gives you ability to control multiple profiles which can hold different logins and environments. You can leave this as it is.
    - **WA_DAILY_LIMIT** - (Optional) The daily limit, script will check if your messages for a day cross this limit and if it does it will stop. This helps avoid sending unlimited messages, which can get your account blocked. 
    - **WHATSAPP_MESSAGE** - (Required) This is the message which you want to send to users. if you want more formatting then visit https://whatsapp-editor.firebaseapp.com
    - **WHATSAPP_ATTACHMENT** - (Optional) If you also want to send the attachment with the message, then just provide the attachment path. Make sure that path is exact format of r"your_path". starts with r.
- Once config file is updated correctly, you can run the script by typing ```python whatsapp_automation.py``` for sending messages to whatsapp users.
- An table with name whatsapp_user_data will be created if you run the script first time. now upload the phone numbers in this table, so that script can start sending messages to those numbers.

### 2. Usage for Email Automation
- Update the config.py
  - Update the **DB_CONNECTION_URI** with your database details if not already done. An example to connect to MS SQL is already commented out
  - Then in EmailConfig class, update the config according to your requirements. Below are details about variables.
    - **HOST** - (Required) This is the smtp host address, e.g smtp.gmail.com
    - **SMTP_PORT** - (Required) This is the smtp port, mostly it is 465 for ssl.
    - **SMTP_EMAIL** - (Required) This is the email id which needs to be used to authenticate with email server
    - **SMTP_PASSWORD** - (Required) This is the password which needs to be used to authenticate with email server
    - **EMAIL_DAILY_LIMIT** - (Required) This will let you control the limit on how many emails you want to send daily.
    - **EMAIL_TEMPLATE_NAME** - (Required) This is the body of email, i.e. email contents in html format. HTML give capability for more customization in email. Below are few websites which you can use to write and format your email and then get the html code for it.
      - https://wordtohtml.net/site/index
      - https://www.textfixer.com/html/convert-email-to-html.php
      - https://www.tiny.cloud/
    - **SUBJECT** - (Required) - This is your email subject
    - **ATTACHMENT_PATH** - (Optional) - If you want to send the attachment with your email, the add the attachment path here or keep it None. You can also add multiple attachments by separating the path using **;** as delimiter. E.g. r"attachment_path1;attachment_path2;attachment_path3"
- Once config file is updated correctly, you can run the script by typing ```python email_automation.py``` for sending emails to users.
- An table with name email_user_data will be created if you run the script first time. now upload the email ids in this table, so that script can start sending emails to those email addresses.

## Note 
Since this is an unofficial way of running your campaigns using personal accounts, it may get your account banned.
This script is just for educational purpose and I am not responsible for any misuse of it.

## Support

- If you face any issue or bug, you can create an issue describing the error message and steps to reproduce the same error, with log file attached.

Please [open an issue](https://github.com/CraftyPythonDeveloper/aws-appstore-automation/issues/new) for support.

## Contributing

Please contribute by create a branch, add commits, and [open a pull request](https://github.com/CraftyPythonDeveloper/aws-appstore-automation/pulls).