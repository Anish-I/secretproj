def our_function(bot_name,csv_file_path):
    print(csv_file_path)
    import time
    import csv
    import os
    import zipfile
    from multiprocessing import Process
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
    from login_handling import login_to_insta, load_cookies
    import pyperclip
    from selenium.webdriver.chrome.options import Options
    import random

    if not os.path.exists("cookies"):
        os.makedirs("cookies")
    if not os.path.exists("d_data"):
        os.makedirs("d_data")
    def get_message():
        import csv
        import random

        intros = []
        with open(f"needs/message/intro_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                intros.append(row[0])

        bodies = []
        with open(f"needs/message/body_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                bodies.append(row[0])

        outros = []
        with open(f"needs/message/outro_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                outros.append(row[0])

        random_intro = random.choice(intros)
        random_body = random.choice(bodies)
        random_outro = random.choice(outros)

        random_sentence = f"{random_intro} {random_body} {random_outro}"
        # print("Random Sentence:", random_sentence)
        return random_sentence

    def human_like_typing(text, input_field):
        lines = text.split("\n")
        for line in lines:
            for char in line:
                try:
                    input_field.send_keys(char)
                    time.sleep(0.05)  # Reduced typing delay
                except:
                    pyperclip.copy(char)
                    input_field.send_keys(Keys.CONTROL, "v")
                    time.sleep(0.05)  # Reduced typing delay
            input_field.send_keys(Keys.SHIFT + Keys.ENTER)
    
    def check_on_texted_people():
        history = []
        try:
         with open(f"needs/texted_people_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                history.append(row[0])
        except :
            pass
        new = []
        with open(f"needs/users_to_reach_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                new.append(row[0])
        data = False
        for link in new:
            if link not in history:
                data = True
        if data:
            return True
        else:
            return False
    
    def loop_in_customers(driver ,email):
        user_data = []
        with open(f"needs/users_to_reach_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                user_data.append({"Username": row[0], "Full name": row[1]})

        texted_people = []
        try:
         with open(f"needs/texted_people_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                texted_people.append(row[0])
        except :
            pass
        
        try:
            notifications_off = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@class='_a9-- _ap36 _a9_1']")
                )
            )
            if notifications_off:
                notifications_off.click()
                print("clicked not now")
        except:
            print("no ig notification enable message")

        try:
            s_f_a_a_c_m2 = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Allow all cookies']")
                )
            )
            if s_f_a_a_c_m2:
                s_f_a_a_c_m2.click()
        except:
            print("no allow all cookies message")

        try:
            dismiss_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Dismiss']")
                )
            )
            if dismiss_message:
                dismiss_message.click()
                print("clicked dismiss")
        except:
            print("no ig dismiss message")

        dm_count = 0
        with open(f"needs/post_{bot_name}_.txt", "r", encoding="utf-8") as file:
            post_link = file.read()
        driver.get(post_link)
        user_not_found = False

        if not user_not_found:
            dm_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "(//*[local-name()='svg' and (@aria-label='Share' or @aria-label='Share Post')])[last()]",
                    )
                )
            )
            dm_element.click()
            time.sleep(1)
        to_message = []
        for user_info in user_data:
            print(dm_count)
            if dm_count >= 5:
                break
            user_id = user_info["Username"]
            user_Full_name = user_info["Full name"]
            modified_name = user_Full_name

            if user_id not in texted_people:
                with open(
                    f"needs/texted_people_{bot_name}_.csv", "a", newline="", encoding="utf-8"
                ) as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([user_id])
                texted_people.append(user_id)
                texted_people = []
                with open( f"needs/texted_people_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        texted_people.append(row[0])
                with open(f'needs/Numbers_{bot_name}_.txt', 'r',encoding='utf-8') as file:
                    first_line = file.readline().strip()
                limit_of_one_account_str,limitof_thebot_str= first_line.split(',')
                limit_of_account = int(limit_of_one_account_str)
                limit_of_the_bot = int(limitof_thebot_str)
                if len(texted_people) >= limit_of_the_bot:
                    break
                print(f"Sending message to user id: {user_id}")
                time.sleep(1)
                try:
                    retry_count = 0
                    while retry_count < 3:  # Retry mechanism
                        try:
                            search_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME, "queryBox")))
                            human_like_typing(text=user_id, input_field=search_box)

                            time.sleep(1)
                            choose_the_ids = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located(
                                    (
                                        By.XPATH,
                                        f"//span[@class='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft' and text()='{user_id}']",
                                    )
                                )
                            )
                            if not choose_the_ids:
                                raise TimeoutException
                            else:
                                user_not_found = False

                            for choose_the_id in choose_the_ids:
                                choose_the_id.click()
                                time.sleep(1)

                            time.sleep(1)
                            dm_count += 1
                            to_message.append(
                                {"Username": user_id, "Full name": modified_name}
                            )
                            break  # Exit retry loop if successful
                        except TimeoutException:
                            print(
                                f"User {user_id} not found, deleting typed username and moving to next."
                            )
                            search_box.send_keys(Keys.CONTROL + "a")
                            search_box.send_keys(Keys.DELETE)
                            user_not_found = True
                            break  # Move to the next user
                        except Exception as e:
                            print(f"Exception occurred while clicking: {e}")
                            time.sleep(2)  # Wait before retrying
                            driver.get(post_link)
                            retry_count += 1
                    else:
                        continue  # Move to the next user if retries are exhausted
                except Exception as e:
                    user_not_found = False
                    driver.get(post_link)
                    print(f"Timed out waiting for the icon to be present. {e}")
        time.sleep(2)
        try:
            send_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'xh8yej3 x1tu34mt xzloghq') and @role='button']",
                    )
                )
            )
            send_button.click()
        except Exception as e:
            print(f"A7A WE GOT ERRPR {e}")
        time.sleep(7)
        dm_count2 = 0
        url = "https://www.instagram.com/direct/inbox/"
        try:
            message_buttons = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[local-name()='svg' and @aria-label='Direct']")
                )
            )
            if message_buttons:
                time.sleep(2)
                message_buttons.click()
        except:
            driver.get(url)
        i_ = 0
        for user_info2 in to_message[::-1]:
            user_id2 = user_info2["Username"]
            user_Full_name = user_info2["Full name"]
            modified_name = user_Full_name
            print(modified_name)
            try:
                if user_id2:
                    scroll_down_dat = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                '//div[contains(@class ,"x78zum5 xdt5ytf x1iyjqo2 xs83m0k x1xzczws x6ikm8r ")]',
                            )
                        )
                    )

                    list_element = scroll_down_dat.find_elements(
                        By.XPATH, '//div[@class="x13dflua x19991ni"]'
                    )
                    try:
                        print(i_)
                        user_name_text = ""
                        try:
                            driver.execute_script(
                                "arguments[0].scrollIntoView(true);", list_element[i_]
                            )
                            time.sleep(0.5)
                            list_element[i_].click()
                        except Exception as e:
                            print(i_)
                            print(f"no new user yet {e}")
                        time.sleep(3)
                        message_enter = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, ".x1n2onr6 [contenteditable=true]")
                            )
                        )
                        text_content = get_message()
                        message = text_content.replace('<Acount-name>', modified_name)
                        # human_like_typing(text=message, input_field=message_enter)
                        pyperclip.copy(message)
                        message_enter.send_keys(Keys.CONTROL, "v")
                        time.sleep(1)
                        message_enter.send_keys(Keys.ENTER)
                        time.sleep(3)
                    except Exception as e:
                        print(e)
                    i_ += 1

            except Exception as e:
                print(f"error in this part {e}")
        if to_message:
         add_num(csv_file_path, email)
        print("Finished sending DMs")
      
    def get_webdriver_with_proxy():
        proxy_host, proxy_port, user_name, password = "", "", "", ""
        try:
            with open(f"needs/proxy_{bot_name}_.txt", "r", encoding="utf-8") as file:
                # file.readline()
                second_line = file.readline().strip()
            proxy_host, proxy_port, user_name, password = second_line.split(",")
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

        pluginfile = f'proxy_auth_plugin_{bot_name}.zip'

        with zipfile.ZipFile(pluginfile, "w") as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

       
        def cleanup_temp_directory(temp_dir):
            import shutil
            print("Cleaning up temporary directory:", temp_dir)
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    shutil.rmtree(dir_path)
                    
        co = webdriver.ChromeOptions()
        temp_dir = os.getcwd().replace('\\','/') + '/'
        temp_dir=f"{temp_dir}profiles/dont touch_{bot_name}_"
        cleanup_temp_directory(temp_dir)
        print('start')
        co.add_argument("--disable-notifications")
        co.add_argument('--ignore-certificate-errors')
        # co.add_argument("--force-dark-mode=false")
        co.add_argument("--lang=en")
        co.add_argument(f"--user-data-dir={temp_dir}")
        co.add_extension(pluginfile)
        # prefs = {"profile.default_content_setting_values.cookies": 2}
        # co.add_experimental_option("prefs", prefs)
        
        # Launch Chrome with white mode enforced
        # co.add_argument('--blink-settings=darkMode=0')
        
        driver = webdriver.Chrome(options=co)
        driver.get("https://www.instagram.com/")
        return driver

    def value_to_remove_fun(value_to_remove, csv_file_ ):
     # Read data from CSV and filter out the line to remove
                with open(csv_file_, 'r', newline='',encoding='utf-8') as infile:
                    csvreader = csv.reader(infile)
                    rows = [row for row in csvreader if row[0] != value_to_remove]

                # Write back the filtered data to the CSV file
                with open(csv_file_, 'w', newline='',encoding='utf-8') as outfile:
                    csvwriter = csv.writer(outfile)
                    csvwriter.writerows(rows)
        
    def print_only_younger_and_equals(csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)  # Read all rows into a list

        data = []
        numbers_in_row_3 = []

        # Gather all numbers from row[3]
        for row in rows:
            if len(row) <= 5:
                row.append('0')  # Default to '0' if missing

            try:
                num = int(row[5])
            except ValueError:
                num = 0  # Default to '0' if not an integer

            numbers_in_row_3.append(num)

        # Check if all numbers reach 50
        with open(f'needs/Numbers_{bot_name}_.txt', 'r',encoding='utf-8') as file:
            first_line = file.readline().strip()
        limit_of_one_account_str,limitof_thebot_str= first_line.split(',')
        limit_of_account = int(limit_of_one_account_str)
        limit_of_the_bot = int(limitof_thebot_str)
        if limit_of_account > 50:
            limit_of_account = 50
        if all(num >= limit_of_account for num in numbers_in_row_3):
            for row in rows:
                row[5] = '0'
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as outfile:
             writer = csv.writer(outfile)
             writer.writerows(rows) 
            print("stop")

        else:
            # Find the smallest number in row[3]
            smallest_number = min(numbers_in_row_3)
            for row in rows:
                if int(row[5]) == smallest_number:
                    data.append(row)

        return data
        
    def add_num(csv_file_path, user_name):
        # Read the CSV file into a list of lists
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            rows = list(reader)  # Read all rows into a list
            # print(rows)

        # Modify the 'account valid' state for the specified user
        for row in rows:
            if row[0] == user_name:
                if len(row) <= 5:
                    row.append('0')  # Ensure the 4th element exists and is '0'
                try:
                    data = int(row[5])
                    full_num = data + 5
                except ValueError:
                    print('ValueError encountered')
                    full_num = 5
                row[5] = str(full_num)

        # Write the modified rows back to the original CSV file
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)  # Write the modified rows

              
    def actions_needed(csv_file_path):
      result = print_only_younger_and_equals(csv_file_path)
      if result:
        for email_data in result:
            email = email_data[0]
            password = email_data[1]
            numbers=email_data[3]
            texted_people = []
            try:
             with open(f"needs/texted_people_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    texted_people.append(row[0])
            except:
                pass
            with open(f'needs/Numbers_{bot_name}_.txt', 'r',encoding='utf-8') as file:
                first_line = file.readline().strip()
            limit_of_one_account_str,limitof_thebot_str= first_line.split(',')
            limit_of_account = int(limit_of_one_account_str)
            limit_of_the_bot = int(limitof_thebot_str)
            if len(texted_people) >= limit_of_the_bot:
                print(f'reached bots limit {limit_of_the_bot}')
                break
            if check_on_texted_people():
             driver = get_webdriver_with_proxy()
             try:
                file_name = f"{email}.txt"
                file_path = os.path.join("cookies", file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write("[]")
                time.sleep(1)
                load_cookies(driver, file_name)
                driver.get("https://www.instagram.com/")
                skip=False
                try:
                    make_sure_we_logged_in = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "(//*[name()='svg'][@aria-label='Home'])[1]")
                        )
                    )
                    if make_sure_we_logged_in:
                        print("we already logged in before")
                except Exception as e:
                    print("we need to login")
                    if not login_to_insta(email, password):
                        skip=True
                        value_to_remove_fun(email, csv_file_path )
                        from tkinter import messagebox
                        messagebox.showinfo("warning",f"deleted this account {email} its not valid")

                if not skip:    
                 if not make_sure_we_logged_in:
                    time.sleep(1)
                    load_cookies(driver, file_name)
                    driver.refresh()
                 try:
                    loop_in_customers(driver,email)
                 except Exception as e:
                    print(f"Exception occurred: {e}")
             finally:
                if driver is not None:
                    driver.quit()

             print("Wait 1s")
             time.sleep(1)
            else:
                print('No new leads')
        print("Finished all accounts.")

      else:
            print('finished')
            with open(f'got_messages_{bot_name}_.csv','w',encoding='utf-8')as f:
                f.write('stop')
            # break  

    actions_needed(csv_file_path)

def worker_1(bot_name,csv_file_path):
 import csv
 import time
 while True:
        user_data = []
        with open(f"needs/users_to_reach_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                user_data.append({'Username': row[0]})
        
        texted_people = []
        try:
         with open(f"needs/texted_people_{bot_name}_.csv", "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                texted_people.append(row[0])
        except:
            pass

        hehehehe= False
        for user in user_data:
             use = user["Username"]
             if use not in texted_people:
                  our_function(bot_name,csv_file_path)
                  hehehehe = True
        with open(f'needs/Numbers_{bot_name}_.txt', 'r',encoding='utf-8') as file:
            first_line = file.readline().strip()
        limit_of_one_account_str,limitof_thebot_str= first_line.split(',')
        limit_of_account = int(limit_of_one_account_str)
        limit_of_the_bot = int(limitof_thebot_str)
        if len(texted_people) >= limit_of_the_bot:
            print("Reached Limit u made for the Bot")
            break
        checker_data=''
        with open(f'got_messages_{bot_name}_.csv','r',encoding='utf-8')as f:
               checker_data=f.readline().strip()
        if checker_data == 'stop':
            print('bot is done')
            break 
            
        if not hehehehe :  
             print('checking for new customers')
             
        time.sleep(10)

