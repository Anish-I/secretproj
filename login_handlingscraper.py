
def login_to_insta(email, password,bot_name):
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
    with open(f'needs/Numbers_sleep_in_test_scraper_{bot_name}_.txt', 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
    min_minute_str,ok = first_line.split(',')
    min_minute = int(min_minute_str)
    if min_minute:
        pass
    else:
        min_minute=1
    print(f'sleeping for {min_minute} s ')
    time.sleep(min_minute)
   
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
