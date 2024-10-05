import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta, timezone
import csv

# Configuration for IMAP (retrieving emails)
def get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD):
    IMAP_SERVER = 'imap.rambler.ru'
    IMAP_PORT = 993
    # Connect to IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

    # Select the inbox folder
    mail.select('inbox')

    # Get the current UTC time and the time 5 minutes ago
    current_time = datetime.now(timezone.utc)
    five_minutes_ago = current_time - timedelta(minutes=5)

    # Format the time to the IMAP-compatible format (DD-Mon-YYYY)
    search_since = five_minutes_ago.strftime('%d-%b-%Y')

    # Search for emails in the last 5 minutes (using the "SINCE" criterion)
    search_criteria = f'(SINCE {search_since})'
    result, data = mail.search(None, search_criteria)

    # Open the file in read mode
    history = []
    try:
        with open('history.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            # Loop through the rows and print them
            for row in reader:
                history.append(row[0])
    except:
        pass

    mail_ids = data[0].split()
    if not mail_ids:
        print("No emails received in the last 5 minutes.")
    else:
        verification_codes=[]
        for mail_id in mail_ids:
            checker = f'{EMAIL_ACCOUNT}_{mail_id}'
            if checker not in history:
                # Fetch each email
                result, msg_data = mail.fetch(mail_id, '(RFC822)')
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Decode email subject
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or 'utf-8')

                # Get the sender of the email
                sender = msg.get('From')

                # Get the email body
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(
                                decode=True).decode('utf-8')
                            break
                else:
                    body = msg.get_payload(decode=True).decode('utf-8')

                # Print the subject, sender, and body of the email
                print(f'Subject: {subject}')
                print(f'From: {sender}')
                # print(f'Body: {body}')
                print('-' * 50)

                # Open the file in append mode
                with open('history.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([f'{EMAIL_ACCOUNT}_{mail_id}',])
                code=get_the_code(body)
                if code :
                    verification_codes.append(code)

            else:
                print('retrived thie mail before ')

    # Logout
    mail.logout()
    return verification_codes


def get_the_code(html_content):
    import re
    # Regular expression to find 6-digit numbers
    code_match = re.search(r'\b\d{6}\b', html_content)

    # Check if a code was found
    if code_match:
        confirmation_code = code_match.group()
        print(f"Confirmation Code: {confirmation_code.strip()}")
        return confirmation_code.strip()
    else:
        print("No confirmation code found.")
        return

def change_password(csv_file_path,user_name,new_password):
        # Read the CSV file into a list of lists
        with open(csv_file_path, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)  # Read all rows into a list

        # Modify the 'account valid' state for the specified user
        for row in rows:
            if row[0] == user_name:
                row[1] = new_password

        # Write the modified rows back to the original CSV file
        with open(csv_file_path, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)  # Write the modified rows

# This code to handel the autologin whcich happens due to insta blocks
def login_to_insta(email, password,bot_name,EMAIL_ACCOUNT,EMAIL_PASSWORD):
    use_rambler=True
    cookies_name=f"{email.replace('@','_')}.txt"
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    import os
    from captcha_solver_selen import captcha_solver
    current_directory = os.getcwd().replace('\\','/') + '/'
    try:
        path = f'{current_directory}extentions/mpbjkejclgfgadiemmefgebjfooflfhl'
        directory_contents = os.listdir(path)
        item = directory_contents[0]
        extension_path3 = f"{current_directory}extentions/mpbjkejclgfgadiemmefgebjfooflfhl/{item}"
    except Exception as e:
        print(e)
    chrome_options3 = Options()
    chrome_options3.add_argument("--disable-notifications")
    chrome_options3.add_argument(f'--load-extension={extension_path3}')
    chrome_options3.add_argument('--lang=en')
    driver3 = webdriver.Chrome(options=chrome_options3)
    login = "https://www.instagram.com/accounts/login/"
    driver3.get(login)
    try:
            appeal = WebDriverWait(driver3,10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Appeal']")))
            if appeal:
                time.sleep(2)
                appeal.click()
                print('clicked appeal')
    except:
            print('no ig appeal message')
    captcha_solver(driver3, WebDriverWait, EC, time, By)
    try:
        click_next=WebDriverWait(driver3,10).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Next']")))
        time.sleep(1)
        if click_next:
            click_next.click()
            print('we clicked next')
    except Exception as e:
        print("no click next ")
     
    try:
        enter_email=WebDriverWait(driver3,10).until(
                                EC.presence_of_element_located((By.XPATH, "//input[@dir='auto' and @placeholder='Email']")))
        time.sleep(1)
        enter_email.send_keys(EMAIL_ACCOUNT)
        time.sleep(2)
        send_code=WebDriverWait(driver3,10).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Send code']")))
        time.sleep(1)
        send_code.click()
        print('clicked send code')
        time.sleep(10)
        codes = get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        if codes :
            print(f'this is the code {codes[-1]}')
            enter_code = WebDriverWait(driver3,5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@maxlength='6']")))
            if enter_code: 
                    for sub_code in codes[-1]:
                        enter_code.send_keys(sub_code)
                        time.sleep(0.1)
        medo=True
        if medo:
                submit_button = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Next']")))
                if submit_button:
                 time.sleep(1)
                 submit_button.click()
                try:
                    print('check if code is ok')
                    make_sure_code_is_ok=WebDriverWait(driver3,10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Error: You have entered an incorrect confirmation code. Please enter the same confirmation code that we sent to your email address.']")))
                    if make_sure_code_is_ok:
                        get_new_code = WebDriverWait(driver3,5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Request new code' and @role='button']")))
                        if get_new_code:
                            time.sleep(2)
                            get_new_code.click()
                            print('clicked request new code') 
                            time.sleep(10)
                            codes = get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                            if codes :
                                print(f'this is the code {codes[-1]}')
                                enter_code = WebDriverWait(driver3,5).until(
                                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Security code']")))
                                if enter_code: 
                                    for sub_code in codes[-1]:
                                        enter_code.send_keys(sub_code)
                                        time.sleep(0.1)
                                submit_button = WebDriverWait(driver3,5).until(
                                    EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Next']")))
                                if submit_button:
                                 time.sleep(1)
                                 submit_button.click()
                                time.sleep(1000)

                except:
                    print('the code was ok')
                try:
                    print('see if ask to make new pass')
                    ask_make_new_pass = WebDriverWait(driver3,20).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='New password']")))
                    if ask_make_new_pass:
                     time.sleep(1)
                    #  new_pass=
                     ask_make_new_pass.send_keys(f'{password}Aa')
                     ask_make_new_pass2 = WebDriverWait(driver3,10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='New password confirmation']")))
                     if ask_make_new_pass2:
                      time.sleep(1)
                      ask_make_new_pass2.send_keys(f'{password}Aa')
                     next_button_a = WebDriverWait(driver3,10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Next']")))
                     if next_button_a:
                      time.sleep(1)
                      next_button_a.click()
                     print('password changed')
                     csv_file_path = f'needs/bot_{bot_name}_.csv'
                     change_password(csv_file_path,email,f'{password}Aa')
                except:
                    print('no change password request present')
                    pass
                try:
                    get_new_code = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='Get a new one']")))
                    if get_new_code:
                        time.sleep(2)
                        get_new_code.click()
                        print('clicked Cotinue') 
                        time.sleep(10)
                        codes = get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                        if codes :
                            print(f'this is the code {codes[-1]}')
                            enter_code = WebDriverWait(driver3,5).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Security code']")))
                            if enter_code: 
                                for sub_code in codes[-1]:
                                    enter_code.send_keys(sub_code)
                                    time.sleep(0.1)
                            submit_button = WebDriverWait(driver3,5).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Submit']")))
                            if submit_button:
                             time.sleep(1)
                             submit_button.click()
                except:
                    print('we succeded in first try')

    except:
        print('no enter email')


    driver3.switch_to.default_content()



    # Locate the username and password input fields and the login button
    username_input = WebDriverWait(driver3, 20).until(
        EC.presence_of_element_located((By.NAME, "username")))
    password_input = WebDriverWait(driver3, 20).until(
        EC.presence_of_element_located((By.NAME, "password")))
    login_button = WebDriverWait(driver3, 20).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, "button[type='submit']")))
    username_input.send_keys(email)
    time.sleep(2)
    password_input.send_keys(password)
    time.sleep(3)
    login_button.click()
    with open(f'needs/Numbers_sleep_in_test_{bot_name}_.txt', 'r',encoding='utf-8') as file:
        first_line = file.readline().strip()
    min_minute_str,ok = first_line.split(',')
    min_minute = int(min_minute_str)
    if min_minute:
        pass
    else:
        min_minute=1
    print(f'sleeping for {min_minute} s ')
    time.sleep(min_minute)

    if use_rambler:
     try:
         print('see if suspicous login')
         suspicsuous = WebDriverWait(driver3,17).until(
                    EC.presence_of_element_located((By.XPATH, "//p[text()='Suspicious Login Attempt']")))
         if suspicsuous :
               print('suspicous login')
               contintue_button = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Continue']")))
               if contintue_button:
                time.sleep(2)
                contintue_button.click()
                print('clicked Cotinue') 
                time.sleep(10)
                codes = get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                if codes :
                    print(f'this is the code {codes[-1]}')
                    enter_code = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Security code']")))
                    if enter_code: 
                         for sub_code in codes[-1]:
                              enter_code.send_keys(sub_code)
                              time.sleep(0.1)
                else:
                    get_new_code = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='Get a new one']")))
                    if get_new_code:
                        time.sleep(2)
                        get_new_code.click()
                        print('clicked Cotinue') 
                        time.sleep(10)
                        codes = get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                        if codes :
                            print(f'this is the code {codes[-1]}')
                            enter_code = WebDriverWait(driver3,5).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Security code']")))
                            if enter_code: 
                                for sub_code in codes[-1]:
                                    enter_code.send_keys(sub_code)
                                    time.sleep(0.1)
                submit_button = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Submit']")))
                if submit_button:
                 time.sleep(1)
                 submit_button.click()
                try:
                    print('see if ask to make new pass')
                    ask_make_new_pass = WebDriverWait(driver3,20).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='New password']")))
                    if ask_make_new_pass:
                     time.sleep(1)
                    #  new_pass=
                     ask_make_new_pass.send_keys(f'{password}Aa')
                     ask_make_new_pass2 = WebDriverWait(driver3,10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='New password confirmation']")))
                     if ask_make_new_pass2:
                      time.sleep(1)
                      ask_make_new_pass2.send_keys(f'{password}Aa')
                     next_button_a = WebDriverWait(driver3,10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Next']")))
                     if next_button_a:
                      time.sleep(1)
                      next_button_a.click()
                     print('password changed')
                     csv_file_path = f'needs/bot_{bot_name}_.csv'
                     change_password(csv_file_path,email,f'{password}Aa')
                except:
                    print('no change password request present')
                    pass
                try:
                    get_new_code = WebDriverWait(driver3,5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='Get a new one']")))
                    if get_new_code:
                        time.sleep(2)
                        get_new_code.click()
                        print('clicked Cotinue') 
                        time.sleep(10)
                        codes = get_emails_last_5_minutes(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                        if codes :
                            print(f'this is the code {codes[-1]}')
                            enter_code = WebDriverWait(driver3,5).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Security code']")))
                            if enter_code: 
                                for sub_code in codes[-1]:
                                    enter_code.send_keys(sub_code)
                                    time.sleep(0.1)
                            submit_button = WebDriverWait(driver3,5).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Submit']")))
                            if submit_button:
                             time.sleep(1)
                             submit_button.click()
                except:
                    print('we succeded in first try')
     except:
        print('no suspicous login ')
    else:
        print('no use rambler')
    try:
            dismmis_message = WebDriverWait(driver3,10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Dismiss']")))
            if dismmis_message:
                time.sleep(2)
                dismmis_message.click()
                print('clicked dismiss')
    except:
            print('no ig dismiss message')
    captcha_solver(driver3, WebDriverWait, EC, time, By)
    try:
        click_next=WebDriverWait(driver3,5).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x9bdzbf x1ypdohk x78zum5 x1f6kntn xwhw2v2 x10w6t97 xl56j7k x17ydfre x1swvt13 x1pi30zi x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye x1tu34mt xzloghq'][1]")))
        time.sleep(1)
        try:
            click_next.click()
            print('we clicked next')
        except:
            try:
                print('2nd try to click next ')
                click_next = WebDriverWait(driver3, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='button']")))
                time.sleep(1)
                
                click_next.click()
            except Exception as e:
                print("error click next 2:")
    except Exception as e:
        print("no click next ")
    driver3.switch_to.default_content()
    time.sleep(10)
    a7a=True
    try:
     search_button = WebDriverWait(driver3, 3).until(
                        EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@aria-label='Search'])[1]")))
     print('loged in successfully')
    except :
        print('your are not loged in')
        a7a=False
    if a7a:
        cookies = driver3.get_cookies()
        with open(f"cookies/{cookies_name}", "w", encoding="utf-8") as f:
            f.write(str(cookies))
        print('we got the cookies')
    driver3.quit()
    return a7a




def load_cookies(driver, cookies_name):
    with open(f"cookies/{cookies_name}", "r", encoding="utf-8") as f:
        cookies = eval(f.read())
    for cookie in cookies:
        driver.add_cookie(cookie)
    print(f'cookies loaded of {cookies_name}')
