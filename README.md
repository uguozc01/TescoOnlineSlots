TABLE OF CONTENTS:

    General Info
    Prerequisites
    Setup
    Technologies
    Usage


GENERAL INFO

    Tesco Online shopping slot finder app simply finds any hourly slots in provided three weeks slot matrix


PREREQUISITES

    An existing Gmail Address
    A registered Tesco User for online shopping
    Chromedriver to run this program by using google chrome browser
    Python3.6 or higher version
    Selenium Python library
    SMTP library


TECHNOLOGIES

    Python coding and Selenium library has been used. 
    Object Oriented Programming could be used too. 
    For OOP we wimply need to create four different classes: Page, Element, Locators, Setup

    We can collect all locators in a Locators class
    We can find all elements by using an Element class
    We can keep all different pages in a Page class (like main page, log-in page etc)
    We can initialise everything by using a setup class which will also include setup, tear-down functions etc


SETUP

    To run this project, 
    install 
        python 3.6 or higher version,
        selenium 3.141.0 library
        smtplib to send emails

    1. Create a Tesco Online shopping username TESCO_USER and password TESCO_PASS
    and set them as env variables:
        export TESCO_USER="email@gmail.com"     # if you used gmail 
        export TESCO_PASS="yourtescopasswd"
    
    They are fetched from .bash_profile like the following:
        USER = os.environ.get('TESCO_USER')
        PASS = os.environ.get('TESCO_PASS')
    
    2. Also create a device access to your computer where you will be using this application. Simply you need to create 
    a new application password for your computer by logging into gmail account settings -> Security -> App passwords

    Refer to : https://support.google.com/accounts/answer/185833?hl=en

    Gmail gives 16 character long app password for your pc. See how to keep it safe in the following item 3

    3. Create EMAIL_USER and EMAIL_PASS environment variables for GMAIL for security purpose:
        export EMAIL_USER="email@gmail.com"
        export EMAIL_PASS="abcdefghijklmnop"    # Gmail gives 16 character long app password for your pc

    They are used in the code like the following:
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    4. Create a gmail smtp access for your gmail address. Refer to : https://support.google.com/mail/answer/7126229?hl=en-GB
    You have to create access to smtp.gmail.com by logging into Gmail Settings

    For this you need to use either 
    port for SSL: 465 or 
    port for TLS/STARTTLS: 587 
    in this project I have used 465. 

    5. Be sure that you have installed Chromedriver, check:
        /usr/bin/chromedriver


USAGE
    
    python3 slot_finder.py