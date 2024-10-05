# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# extension_path1 = "C:/Users/moham/AppData/Local/Google/Chrome/User Data/Default/Extensions/mpbjkejclgfgadiemmefgebjfooflfhl/2.0.1_0"
# chrome_options = Options()
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument(f'--load-extension={extension_path1}')
# # chrome_options.add_argument('--ignore-certificate-errors')
# # chrome_options.add_argument("--user-data-dir=D:\\aa\\a1\\a1")
# driver = webdriver.Chrome(options=chrome_options)
# url = "https://www.google.com/recaptcha/api2/demo"
# driver.get(url)

import pyautogui
from selenium.common.exceptions import TimeoutException

def captcha_solver(driver, WebDriverWait, EC, time, By):
    print('searching if captcha found')
    try:
        # this first iframe for insta only iframe_0
        iframe_0 = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[@id='recaptcha-iframe']")))
        driver.switch_to.frame(iframe_0)
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]:first-of-type')))
        if iframe:
            driver.switch_to.frame(iframe)
            print('switched the i frame')
            click_captcha = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='recaptcha-checkbox-border']")))
            print("try to click it")
            if click_captcha:
                time.sleep(3)
                try:
                    click_captcha.click()
                    print('captcha clicked')
                except Exception as e:
                    print(f'a7a {e}')
            check_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.recaptcha-checkbox.goog-inline-block.recaptcha-checkbox-unchecked.rc-anchor-checkbox')))
            if 'recaptcha-checkbox-checked' not in check_box.get_attribute('class'):
                try:
                    pyautogui.moveTo((280, 387), duration=1)
                    driver.switch_to.default_content()
                    # this first iframe for insta only iframe_0
                    iframe_0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                        (By.XPATH, "//iframe[@id='recaptcha-iframe']")))
                    driver.switch_to.frame(iframe_0)
                    print('switched')
                    iframe2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]')))
                    if iframe2:
                        pyautogui.moveTo((270, 387), duration=1)
                        driver.switch_to.frame(iframe2)
                        print('switched the i frame2')
                        try:
                            # time.sleep(1000)
                            click_the_solve = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@class='button-holder help-button-holder']")))
                            if click_the_solve:
                                time.sleep(1)
                                pyautogui.moveTo((410, 510), duration=1)
                                click_the_solve.click()
                                time.sleep(3)
                                i = 0
                                while True:
                                    i += 1
                                    try:
                                        try:
                                            click_the_solve = WebDriverWait(driver, 0.5).until(
                                                EC.presence_of_element_located((By.XPATH, "//div[@class='button-holder help-button-holder']")))
                                            if click_the_solve:
                                                try:
                                                    print("try to click again")
                                                    click_the_solve.click()
                                                except :
                                                    print('try')
                                                   #  break
                                            else:
                                                print('no click solve')
                                                break
                                        except TimeoutException:
                                            print('not avilable')
                                            break
                                        time.sleep(3)
                                        if i % 2 == 0:
                                            print('we got 2 tries')
                                            click_reload = WebDriverWait(driver, 5).until(
                                                EC.presence_of_element_located((By.XPATH, "//button[@id='recaptcha-reload-button']")))
                                            if click_reload:
                                                try:
                                                    click_reload.click()
                                                except:
                                                    print(
                                                        "couldnt refresh")
                                                    break
                                            else:
                                                print('no click reload')
                                                break
                                    except:
                                        print('nope')
                                        break
                        except Exception as e:
                            print(f'no man {e}')
                except:
                    print("no 2")

            driver.switch_to.default_content()
            print('back to main page')
    except Exception as e:
        print(f'no captcha')
    try:
        print('make sure we solved the captcha')
        # this first iframe for insta only iframe_0
        iframe_0 = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[@id='recaptcha-iframe']")))
        driver.switch_to.frame(iframe_0)
        iframe = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]:first-of-type')))
        # time.sleep(5)
        if iframe:
            driver.switch_to.frame(iframe)
            check_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.recaptcha-checkbox.goog-inline-block.recaptcha-checkbox-unchecked.rc-anchor-checkbox')))
            if 'recaptcha-checkbox-checked' not in check_box.get_attribute('class'):
                try:
                    driver.switch_to.default_content()
                    # this first iframe for insta only iframe_0
                    iframe_0 = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                        (By.XPATH, "//iframe[@id='recaptcha-iframe']")))
                    driver.switch_to.frame(iframe_0)
                    iframe2 = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]')))
                    if iframe2:
                        pyautogui.moveTo((270, 387), duration=1)
                        driver.switch_to.frame(iframe2)
                        try:
                            click_reset = WebDriverWait(driver, 1).until(
                                EC.presence_of_element_located((By.XPATH, "//button[@title='Reset the challenge']")))
                            if click_reset:
                                click_reset.click()
                        except:
                            print("not present")
                except:
                    print('not present 2')
                driver.switch_to.default_content()
                pyautogui.moveTo((280, 387), duration=1)
                pyautogui.moveTo((270, 387), duration=1)
                pyautogui.moveTo((270, 397), duration=1)
                # pyautogui.leftClick((280, 387))
                pyautogui.moveTo((270, 387), duration=1)
                pyautogui.moveTo((280, 387), duration=1)
                pyautogui.moveTo((410, 510), duration=1)
                captcha_solver(driver, WebDriverWait, EC, time, By)
            else:
               print("captcha is solved successflly")
    except Exception as e:
        print(f'no captcha')
    driver.switch_to.default_content()
    print('we are done')

    # time.sleep(100)


# captcha_solver(driver, WebDriverWait, EC, time, By)

# captcha_solver(driver,WebDriverWait,EC,time,By)
# # time.sleep(100)
# # recaptcha-checkbox-checked
# # //div[@class='button-holder help-button-holder']
# # "recaptcha challenge expires in two minutes"


# # Check if the element doesn't contain the class 'recaptcha-checkbox-checked'
# if 'recaptcha-checkbox-checked' not in check_box.get_attribute('class'):
#     # Your code to execute if the class is not present
#     # For example, you can continue with your operations or skip this part
#     pass
# else:
#     # Your code to execute if the class is present (skip this part)
#     pass
