def main_scraper(type_of_agent, My_hashtag,email, password,tracker,bot_name,extract_profiles):
    import time
    import os
    import csv
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from bs4 import BeautifulSoup
    from process_the_xlsx import proces_excel_files
    from login_handling import login_to_insta, load_cookies
    from selenium.webdriver.common.keys import Keys
    import zipfile

    directory = "data"
    file_path = os.path.join(directory, "data.csv")
    file_path2 = os.path.join(directory, "full_data.csv")
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(
                "Instagram ID,Username,Full name,Profile link,Avatar pic,Followed by viewer,Is verified,Followers count,Following count,Biography,Public email,Posts count,Phone country code,Phone number,City,Address,Is private,Is business,External url\n"
            )  # Example header

    if not os.path.exists(file_path2):
        with open(file_path2, "w", encoding="utf-8") as file:
            file.write(
                "Instagram ID,Username,Full name,Profile link,Avatar pic,Followed by viewer,Is verified,Followers count,Following count,Biography,Public email,Posts count,Phone country code,Phone number,City,Address,Is private,Is business,External url\n"
            )  # Example header

    if not os.path.exists("cookies"):
        os.makedirs("cookies")

    if not os.path.exists("Downloads"):
        os.makedirs("Downloads")
     
    def create_driver():
        proxy_host, proxy_port, user_name, password ='','','',''
        try:
         with open(f'needs/proxy_{email}_scrape_.txt', 'r',encoding='utf-8') as file:
            # file.readline()
            second_line = file.readline().strip()
         proxy_host, proxy_port, user_name, password = second_line.split(',')
        except:
            pass
        PROXY_HOST = proxy_host
        PROXY_PORT = proxy_port
        PROXY_USER = user_name
        PROXY_PASS = password

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Bright Data Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = f"""
        var config = {{
                mode: "fixed_servers",
                rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{PROXY_HOST}",
                    port: parseInt({PROXY_PORT})
                }},
                bypassList: ["localhost"]
                }}
            }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        function callbackFn(details) {{
            return {{
                authCredentials: {{
                    username: "{PROXY_USER}",
                    password: "{PROXY_PASS}"
                }}
            }};
        }}

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {{urls: ["<all_urls>"]}},
                    ['blocking']
        );
        """

        pluginfile = f'proxy_auth_plugin_{bot_name}_scrape.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        

        current_directory = os.getcwd().replace("\\", "/") + "/"
        try:
            path = f"{current_directory}extentions/hndnabgpcmhdmaejoapophbidipmgnpb"
            directory_contents = os.listdir(path)
            item = directory_contents[0]
            extension_path3 = (
                f"{current_directory}extentions/hndnabgpcmhdmaejoapophbidipmgnpb/{item}"
            )
        except Exception as e:
            print(e)

        chrome_options1 = Options()
        chrome_options1.add_argument("--disable-notifications")
        chrome_options1.add_argument("--ignore-certificate-errors")
        chrome_options1.add_argument("--lang=en")
        chrome_options1.add_argument(f"--load-extension={extension_path3}")
        download_directory = f"{current_directory}Downloads".replace("/", "\\")
        prefs = {"download.default_directory": download_directory}
        chrome_options1.add_experimental_option("prefs", prefs)
        chrome_options1.add_extension(pluginfile)

        driver = webdriver.Chrome(options=chrome_options1)
        driver.get('https://www.instagram.com/')
        return driver

    def get_filtered_data_line_count(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                line_count = len(lines) - 1  # Subtracting 1 to account for the header
                print(f"Successfully read {file_path}. Line count: {line_count}")
                return line_count
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return 0

    def get_target_line_count(global_file_path):
        try:
            with open(global_file_path, "r", encoding="utf-8") as file:
                target_count = int(file.readline().strip())
                print(
                    f"Successfully read target line count from {global_file_path}. Target: {target_count}"
                )
                return target_count
        except Exception as e:
            print(f"Error reading {global_file_path}: {e}")
            return 0

    def loop_for_the_error_of_login(driver, email, password, file_name):
        while True:
            try:
                time.sleep(120)

                print("downloading the xlsx file")
                expert_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "mu-ripple-wrapper")
                    )
                )
                expert_buttons[2].click()
                time.sleep(4)
                proces_excel_files(bot_name)
            
                print("Checking for the target element...")
                page_html = driver.page_source
                soup = BeautifulSoup(page_html, "html.parser")
                error_div = soup.find(
                    "div",
                    {
                        "class": "mu-alert mu-error-color mu-inverse",
                        "data-v-116b9c74": True,
                        "style": "margin-top: 20px; margin-bottom: 5px; width: 60%;",
                    },
                )
                if (
                    error_div
                    and "Request failed with status code 401" in error_div.text
                ):
                    login_to_insta(email, password)
                    driver.switch_to.window(driver.window_handles[3])
                    time.sleep(3)
                    load_cookies(driver, file_name)
                    driver.refresh()
                    time.sleep(3)
                    driver.switch_to.window(driver.window_handles[2])
                    print("haha")
                
                if not extract_profiles :
                    try:
                        button = soup.find("button", class_="mu-button mu-icon-button mu-primary-text-color")
                        if button:
                         print('finished scraping')
                         break
                         
                    except:
                        pass
            except TimeoutException:
                print("Timeout: Target element not found.")
           
            

    def open_extention(driver, type_of_agent, My_hashtag, email, password, file_name,tracker):
        url = "https://www.instagram.com/accounts/login/"
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        print("switching")
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        extension_popup_url = (
            "chrome-extension://hndnabgpcmhdmaejoapophbidipmgnpb/popup/popup.html"
        )
        driver.get(extension_popup_url)
        print("working 1")

        # time.sleep(1)
        # diamond = WebDriverWait(driver, 20).until(
        #     EC.presence_of_all_elements_located(
        #         (By.CSS_SELECTOR, "button.mu-button.mu-icon-button")
        #     )
        # )
        # print(len(diamond))
        # while True:
        #     try:
        #         time.sleep(1)
        #         diamond[5].click()
        #         break
        #     except:
        #         pass
        # time.sleep(0.5)
        # Click_here_button = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[text()="Click here."]'))
        # )
        # Click_here_button.click()
        # time.sleep(0.5)
        # inpput_key_field = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, '//input[@class="mu-text-field-input"]')
        #     )
        # )
        # with open("needs/growmankey.txt", "r", encoding="utf-8") as f:
        #     key_data = f.readline()
        # inpput_key_field.send_keys(key_data)
        # time.sleep(0.5)
        # try:
        #  save_button = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.XPATH,
        #             '//button[@class="mu-button mu-raised-button mu-success-color mu-inverse "]',
        #         )
        #     )
        # )
        #  save_button.click()
        # except :
        #     pass
        # time.sleep(3)
        # driver.refresh()
        hashtags = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.mu-button.mu-icon-button")
            )
        )
        while True:
            try:
                hashtags[0].click()
                break
            except:
                pass
        time.sleep(0.5)
        track = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@label='Wait interval(seconds)']")
            )
        )
        track.click()
        if tracker =="no-time":
         try:
            track.send_keys(Keys.ARROW_LEFT * 15)
         except:
            pass
        elif tracker == "max-time":
          try:
            track.send_keys(Keys.ARROW_RIGHT * 15)
          except:
            pass
        elif tracker == "just-before-middile":
          try:
            track.send_keys(Keys.ARROW_LEFT * 9)
          except:
            pass
        elif tracker=='middile':
            pass
        if not  extract_profiles :
            extract_profile=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[@class='mu-checkbox-icon'])[2]")
            ) )
            extract_profile.click()

        time.sleep(2)
        hashtags = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.mu-button.mu-icon-button")
            )
        )
        
        type_of_agent, My_hashtag
        if type_of_agent == "followers":
            radio_button = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "mu-radio-wrapper"))
            )
            radio_button[1].click()
            hashtags[0].click()
            print("getting the followers of this account")
        elif type_of_agent == "following":
            radio_button = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "mu-radio-wrapper"))
            )
            radio_button[1].click()
            hashtags[1].click()
            print("getting the following accounts")
        elif type_of_agent == "hashtag":
            if len(hashtags) >= 3:
                print("working 3")
                hashtags[2].click()
            else:
                print("There are not enough buttons on the page.")
        elif type_of_agent == "location":
            hashtags[3].click()
            print("getting the following accounts")
        
        print("working 4")
        hashtag_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.mu-input input.mu-text-field-input")
            )
        )

        hashtag_input.send_keys(My_hashtag)
        time.sleep(2)
        go_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button.mu-button.mu-raised-button.mu-button-full-width.mu-success-color.mu-inverse",
                )
            )
        )
        go_button.click()
        time.sleep(4)
        print("working 5")
        driver.switch_to.window(driver.window_handles[2])
        print("working 6")
        driver.refresh()
        time.sleep(5)
        if  extract_profiles:
         checkbox_locator = (By.CLASS_NAME, "mu-checkbox")
         checkboxes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(checkbox_locator)
         )
         checkboxes[1].click()
        loop_for_the_error_of_login(driver, email, password, file_name)
        driver.quit()

    def scraper(type_of_agent, My_hashtag, email, password,tracker):
        driver = create_driver()
        driver.get("https://www.instagram.com/")
        file_name = f"{email.replace('@', '_')}.txt"
        file_path = os.path.join("cookies", file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("[]")
        time.sleep(3)
        load_cookies(driver, file_name)
        time.sleep(1)
        driver.get("https://www.instagram.com/")
        try:
            dismmis_message = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Dismiss']")
                )
            )
            if dismmis_message:
                time.sleep(2)
                dismmis_message.click()
                print("clicked dismiss")
        except:
            print("no ig dismiss message")
        make_sure_we_loged_in = ""
        meme = True
        try:
            make_sure_we_loged_in = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//*[name()='svg'][@aria-label='Home'])[1]")
                )
            )
            if make_sure_we_loged_in:
                print("we already loged in before")
        except Exception as e:
            print("we need to login")
            if login_to_insta(email, password):
                meme = True
            else:
                meme = False
        if not make_sure_we_loged_in:
            time.sleep(3)
            load_cookies(driver, file_name)
            time.sleep(1)
            driver.refresh()
            time.sleep(5)
        if meme:
            open_extention(
                driver, type_of_agent, My_hashtag, email, password, file_name,tracker
            )
        driver.quit()

    scraper(type_of_agent, My_hashtag, email, password,tracker)


# import tkinter as tk
# from tkinter import ttk
# from threading import Thread
# import json
# import os

# def start_scraper():
#     type_of_agent = agent_type_var.get()
#     My_hashtag = hashtag_entry.get()
#     tracker = tracker_var.get()
#     extract_profiles = extract_profiles_var.get()
#     save_settings(type_of_agent, My_hashtag, tracker, extract_profiles)
#     email='meme12221a'
#     password='Mohamed12345'
#     bot_name=''
#     if My_hashtag and email and password:
#         Thread(target=main_scraper, args=(type_of_agent, My_hashtag,email, password,tracker,bot_name,extract_profiles)).start()
#     else:
#         print('add the data')

# def save_settings(type_of_agent, My_hashtag, tracker, extract_profiles):
#     settings = {
#         "type_of_agent": type_of_agent,
#         "My_hashtag": My_hashtag,
#         "tracker": tracker,
#         "extract_profiles": extract_profiles
#     }
#     with open("settings.json", "w") as file:
#         json.dump(settings, file)

# def load_settings():
#     if os.path.exists("settings.json"):
#         with open("settings.json", "r") as file:
#             settings = json.load(file)
#             agent_type_var.set(settings.get("type_of_agent", "followers"))
#             hashtag_entry.insert(0, settings.get("My_hashtag", ""))
#             tracker_var.set(settings.get("tracker", "middile"))
#             extract_profiles_var.set(settings.get("extract_profiles", False))

# # Create the main window
# root = tk.Tk()
# root.title("Instagram Scraper")

# # Create and set variables
# agent_type_var = tk.StringVar(value="followers")
# tracker_var = tk.StringVar(value="middile")
# extract_profiles_var = tk.BooleanVar(value=False)

# # Create widgets
# agent_type_label = tk.Label(root, text="Type of Agent:")
# agent_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# agent_type_menu = ttk.Combobox(root, textvariable=agent_type_var, values=["followers", "following", "hashtag","location"])
# agent_type_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# hashtag_label = tk.Label(root, text="user or hashtag or location link:")
# hashtag_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
# hashtag_entry = tk.Entry(root)
# hashtag_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# tracker_label = tk.Label(root, text="Tracker:")
# tracker_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
# tracker_menu = ttk.Combobox(root, textvariable=tracker_var, values=["no-time", "max-time", "middile","just-before-middile"])
# tracker_menu.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# extract_profiles_check = tk.Checkbutton(root, text="Extract Profiles", variable=extract_profiles_var)
# extract_profiles_check.grid(row=3, column=0, padx=10, pady=10, sticky="w")

# start_button = tk.Button(root, text="Start Scraping", command=start_scraper)
# start_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# load_settings()
# # Start the Tkinter event loop
# root.mainloop()

# main_scraper('followers','gucci','meme12221a','Mohamed12345','middile','bot_QwANtvAM_1',False)
