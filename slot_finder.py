import os
import re
import time
import smtplib
from email.message import EmailMessage
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException

USER = os.environ.get('TESCO_USER')
PASS = os.environ.get('TESCO_PASS')

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

class NoSlotAvailableError(Exception):
    """Base class for other exceptions
    You can simply drive more sub classes"""
    pass

def setup():
    global driver
    try:
        driver = webdriver.Chrome('/usr/bin/chromedriver')
        driver.get('https://www.tesco.com/groceries/en-GB/')
        time.sleep(5)
        driver.set_window_position(0, 0)
        window_size(800, 1000)
    except WebDriverException as e:
        print(e)
    except Exception as e:
        print(e)

def window_size(x,y):
    global driver
    browser_size = driver.set_window_size(x,y)
    s1 = f'{x}'.rjust(5)
    s2 = f'{y}'.rjust(5)
    print(f'\nSETTING BROWSER WIDTH\t: {s1}\nSETTING BROWSER HEIGHT\t: {s2}\n')
    return browser_size

def login():
    global driver
    try:
        wait = WebDriverWait(driver,10)
        CookieAcceptCloseFirst = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-policy__button')))
        CookieAcceptCloseFirst.submit()

        LoginElement = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Sign in')))
        LoginElement.click()

        CookieAcceptCloseSecond = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[1]/div/div[2]/form/button')))
        CookieAcceptCloseSecond.submit()

        UsernameElement = wait.until(EC.presence_of_element_located((By.ID,'username')))
        UsernameElement.clear()
        UsernameElement.send_keys(USER)

        PasswordElement = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        PasswordElement.clear()
        PasswordElement.send_keys(PASS)

        SigninButtonElement = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-component__button')))
        SigninButtonElement.click()
    except NoSuchElementException as e:
        print(e)
    except WebDriverException as e:
        print(e)
    except Exception as e:
        print(e)
        driver.quit()

def book_slot():
    global driver
    try:
        wait = WebDriverWait(driver,5)
        SlotElement = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Book a slot')))
        SlotElement.click()
    except WebDriverException as e:
        print(e)
    except Exception as e:
        print(e)
        driver.quit()

def home_delivery():
    global driver
    xpath_deliver = '//*[@id="main"]/div[1]/div/div[1]/div[3]/div/div/div[1]/a'
    try:
        wait = WebDriverWait(driver,10)
        HomeDeliveryElement = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_deliver))) 
        HomeDeliveryElement.click()
    except WebDriverException as e:
        print(e)
    except Exception as e:
        print(e)
        driver.quit()

def click_colleck():
    """Click and Collect if there is no home delivery option presented"""
    global driver
    xpath_collect = '//*[@id="main"]/div[1]/div/div[1]/div[3]/div/div/div[2]/a'
    try:
        wait = WebDriverWait(driver,10)
        HomeDeliveryElement = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_collect)))        
        HomeDeliveryElement.click()
    except WebDriverException as e:
        print(e)
    except Exception as e:
        print(e)
        driver.quit()
    # mySlot = driver.find_element_by_xpath('//*[@id="slot-matrix"]/div[3]/div[2]/div/div/div[1]/div[2]/ul/li[15]/div/form/button')
    # mySlot.submit()

def locators():
    global driver
    wait = WebDriverWait(driver,10)

    WEEK_PATTERN =  '//*[@id="slot-matrix"]/div[3]/div[1]/ul/li'
    WEEK_XPATHS = [f'{WEEK_PATTERN}[{x}]' for x in [1,2,3]]
    WEEK_HREFS = [f'{WEEK_PATTERN}[{x}]/a' for x in [1,2,3]]
    WEEKS_LIST = [(i, j) for i, j in zip(WEEK_XPATHS, WEEK_HREFS)]
    
    DAY_PATTERN = '//*[@id="slot-matrix"]/div[3]/div[2]/div/div/div[1]/div[1]/div/div[2]/ul/li'
    DAY_XPATHS = [f'{DAY_PATTERN}[{x}]' for x in range(1,8)]
    DAY_HREFS = [f'{DAY_PATTERN}[{x}]/a' for x in range(1,8)]
    DAYS_LIST = [(k, l) for k, l in zip(DAY_XPATHS, DAY_HREFS)]

    DAY_CLASS_OK = 'day-selector__list-item'
    DAY_SELECTED_CLASS = f'{DAY_CLASS_OK} {DAY_CLASS_OK}--selected'
    DAY_UNAVAILABLE_CLASS = f'{DAY_CLASS_OK} {DAY_CLASS_OK}--unavailable'
    DAY_SELECTED_UNAVAILABLE = f'{DAY_CLASS_OK} {DAY_CLASS_OK}--selected {DAY_CLASS_OK}--unavailable'
    
    HOUR_CLASS_OK = 'slot-list--item available'
    HOUR_PATTERN = f'//*[@id="slot-matrix"]/div[3]/div[2]/div/div/div[1]/div[2]/ul/li[@class="slot-list--item available"]/div/form/button'

    with open('Available_Slots.txt', 'w') as f:
        for week, week_ref in WEEKS_LIST:
            try:
                week_element = wait.until(EC.visibility_of_element_located((By.XPATH, week)))
                f.write(f'\n{week_element.text.upper()}\n')  
                week_reference = wait.until(EC.element_to_be_clickable((By.XPATH, week_ref)))
                week_reference.click()
                time.sleep(2)
            except ElementClickInterceptedException as e:
                print(e)
            except WebDriverException as e:
                print(e)
            except Exception as e:
                print(e)

            for day, day_ref in DAYS_LIST:
                try:
                    day_xpath_element = wait.until(EC.visibility_of_element_located((By.XPATH, day)))
                    day_reference = wait.until(EC.visibility_of_element_located((By.XPATH, day_ref)))
                    day_class = day_xpath_element.get_attribute("class")
                except StaleElementReferenceException as e:
                    print(e)
                except WebDriverException as e:
                    print(e)
                except Exception as e:
                    print(e)

                if day_class == DAY_CLASS_OK:
                    day_reference.click()
                    time.sleep(2)

                    global HOURS
                    HOURS = wait.until(EC.presence_of_all_elements_located((By.XPATH, HOUR_PATTERN)))

                    for l, hour in enumerate(HOURS, start=1):
                        global pattern_hour
                        pattern_hour = re.match(r'(\w+ \d\d?\w{2} \w+), (\w{7} \d{2}:\d{2} - \d{2}:\d{2})\.', hour.text)
                        global matched_day, matched_hour
                        matched_day = pattern_hour.group(1)
                        matched_hour = pattern_hour.group(2)
                        if  l == 1:
                            f.write(f'\nAVAILABLE DAY \t\t: {matched_day}\n\nAVAILABLE SLOTS \t: {matched_hour}\n')
                        elif len(HOURS) > 1 and l == len(HOURS):
                            f.write(f'\t\t\t: {matched_hour}\n')
                        elif len(HOURS) > 1 and l < len(HOURS):
                            f.write(f'\t\t\t: {matched_hour}\n')
                        else:
                            print(f'cant imagine this possibility')

                elif day_class == DAY_SELECTED_CLASS:
                    day_reference.click()
                    time.sleep(2)

                    global HOURS_SELECTED
                    HOURS_SELECTED = wait.until(EC.presence_of_all_elements_located((By.XPATH, HOUR_PATTERN)))

                    for l, hour_ref in enumerate(HOURS_SELECTED, start=1):
                        global pattern_hour_selected
                        pattern_hour_selected = re.match(r'(\w+ \d\d?\w{2} \w+), (\w{7} \d{2}:\d{2} - \d{2}:\d{2})\.', hour_ref.text)
                        global matched_day_selected, matched_hour_selected
                        matched_day_selected = pattern_hour_selected.group(1)
                        matched_hour_selected = pattern_hour_selected.group(2)
                        if  l == 1:
                            f.write(f'\nAVAILABLE DAY \t\t: {matched_day_selected}\n\nAVAILABLE SLOTS \t: {matched_hour_selected}\n')
                        elif len(HOURS_SELECTED) > 1 and l == len(HOURS_SELECTED):
                            f.write(f'\t\t\t: {matched_hour_selected}\n')
                        elif len(HOURS_SELECTED) > 1 and l < len(HOURS_SELECTED):
                            f.write(f'\t\t\t: {matched_hour_selected}\n')
                        else:
                            print(f'cant imagine this possibility')

                elif day_class == DAY_UNAVAILABLE_CLASS or day_class == DAY_SELECTED_UNAVAILABLE:
                    global pattern_no_slot
                    pattern_no_slot = re.match(r'(.*)\n(.*)\n(.*)', day_xpath_element.text)
                    global matched_date1, matched_date2, matched_date3
                    matched_date1 = pattern_no_slot.group(1)
                    matched_date2 = pattern_no_slot.group(2)
                    matched_date3 = pattern_no_slot.group(3)
                    m1 = f'{matched_date1}'.ljust(10)
                    m3 = f'{matched_date3}'
                    f.write(f'NO SLOT FOR\t\t: {m1} {m3}\n')
                else:
                    print('THERE MUST BE AN IDENTIFIED "li" CLASS')

            time.sleep(2)

def send_email(email=EMAIL_ADDRESS, passwd=EMAIL_PASSWORD):
    try:
        # contacts = ['YourAddress@gmail.com', 'test@example.com']
        msg = EmailMessage()
        msg['Subject'] = 'Tesco Available Shopping Slots'
        msg['From'] = email
        msg['To'] = email # or just type contacts here
        msg.set_content('Shopping Slot Inspection Results are attached as a text file')
    
        with open('Available_Slots.txt', 'r') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, filename=file_name)
    except Exception as e:
        print(e)
    else:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, passwd)
            # sending the mail 
            smtp.send_message(msg)

def teardown():
    time.sleep(10)
    driver.quit()

setup()
login()
book_slot()
home_delivery()
# click_colleck() # home delivery does not give any slot run this. Make it automatically run
locators()
send_email()
teardown()