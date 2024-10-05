def Worm_up(email, password, bot_name, EMAIL_ACCOUNT, EMAIL_PASSWORD, update_the_profile, worm_the_profile,follow_each_other,accs_list):
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
    from login_handling import login_to_insta, load_cookies
    from selenium.webdriver.common.keys import Keys
    import zipfile
    import subprocess
    import random
    import pyperclip
        
    def generate_delay(min_minutes, max_minutes):
        delay = random.uniform(min_minutes * 60, max_minutes * 60)
        return max(delay, min_minutes * 60)
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

    # def load_cookies(driver, cookies_name):
    #     with open(f"cookies/{cookies_name}", "r", encoding="utf-8") as f:
    #         cookies = eval(f.read())
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)
    #     print(f'cookies loaded of {cookies_name}')
    image_name = 'chefandcocanada.jpg'
    bio_ = 'Hey there every one'
    post_pic = 'medo.jpg'

    upload_pic = image_name
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

    def get_webdriver_with_proxy():
        proxy_host, proxy_port, user_name, password = "", "", "", ""
        try:
            with open(f"needs/proxy_{bot_name}_.txt", "r", encoding="utf-8") as file:
                # file.readline()
                second_line = file.readline().strip()
            proxy_host, proxy_port, user_name, password = second_line.split(
                ",")
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
        temp_dir = os.getcwd().replace('\\', '/') + '/'
        temp_dir = f"{temp_dir}profiles/dont touch_{bot_name}_"
        cleanup_temp_directory(temp_dir)
        print('start')
        co.add_argument("--disable-notifications")
        co.add_argument('--ignore-certificate-errors')
        co.add_argument("--lang=en")
        co.add_argument(f"--user-data-dir={temp_dir}")
        co.add_extension(pluginfile)
        co.add_argument("--disable-webrtc")
        co.add_argument("--disable-webgl")
        co.add_argument("--disable-bundled-ppapi-flash")
        co.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=co)
        return driver

    def value_to_remove_fun(value_to_remove, csv_file_):
        # Read data from CSV and filter out the line to remove
        with open(csv_file_, 'r', newline='', encoding='utf-8') as infile:
            csvreader = csv.reader(infile)
            rows = [row for row in csvreader if row[0] != value_to_remove]

        # Write back the filtered data to the CSV file
        with open(csv_file_, 'w', newline='', encoding='utf-8') as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerows(rows)

    def update_profile(driver, email):

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

        try:
            open_profile = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, f'//a[@href="/{email}/"]')))
            if open_profile:
                open_profile.click()
                print('clicked open profile')
        except Exception as e:
            print(e)
            print('error in open profile')
        add_prof_photo = ''
        try:
            add_prof_photo = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//button[@title="Add a profile photo"]')))
            if add_prof_photo:
                add_prof_photo.click()
                print('clicked add profile photo')
        except Exception as e:
            print(e)
            print('already have a photo')

        def get_the_pics(name):
            formatted_names = '"' + name + '"'
            print(formatted_names)
            return formatted_names
        if add_prof_photo:
            img_path = get_the_pics(upload_pic)
            try:
                current_directory = os.getcwd()
                path = f"{current_directory}\\pics\\"
                path = path.replace("\\", "/")
                print('path of the pics:', path)
                autoit_script_path = 'upload_file1.exe'
                subprocess.run(
                    [autoit_script_path, path, img_path])
                time.sleep(5)
                print('updated profile pic')
            except Exception as e:
                print(f"An error occurred while uploading {img_path}: {e}")
        else:
            print('we already have a profile pic')
        ''''
        create_first_post = ''
        try:
            create_first_post = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="Share your first photo"]')))
            if create_first_post:
                create_first_post.click()
                print('clicked post first post')
                click_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//button[text()='Select from computer']")))
                if click_upload:
                    click_upload.click()
                    print('clicked upload from pc')

        except Exception as e:
            print(e)
            print('already have a post')

        if create_first_post:
            img_path = get_the_pics(post_pic)
            try:
                current_directory = os.getcwd()
                path = f"{current_directory}\\pics\\"
                path = path.replace("\\", "/")
                print('path of the pics:', path)
                autoit_script_path = 'upload_file1.exe'
                subprocess.run(
                    [autoit_script_path, path, img_path])
                time.sleep(5)
                print('uploaded post pic')
            except Exception as e:
                print(f"An error occurred while uploading {img_path}: {e}")
            next_post_the_pic = ''
            try:
                next_post_the_pic = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Next')]")))
                time.sleep(1)
                next_post_the_pic.click()
                print('next')
            except Exception as e:
                print(f"error next_post_the_pic : {e}")
            if next_post_the_pic:
                try:
                    next2_post_the_pic = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Next')]")))
                    time.sleep(1)
                    next2_post_the_pic.click()
                    print('next')
                except Exception as e:
                    print(f"error next2_post_the_pic : {e}")
                try:
                    post_caption_adding = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a caption...']")))
                    human_like_typing('Hello there', post_caption_adding)
                    print('we added a caption for the post')
                except:
                    print('we couldnt add the post caption')
                try:
                    share_button = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "(//div[contains(text(),'Share')])[1]")))
                    time.sleep(1)
                    try:
                        share_button.click()
                        print('we sahred the post')
                    except:
                        try:
                            print('2nd try to click the share shit')
                            share_button = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37']")))
                            time.sleep(1)
                            share_button.click()
                        except Exception as e:
                            print(f"error share_button : {e}")
                except Exception as e:
                    print(f"error share_button : {e}")
                while True:
                    try:
                        post_shared = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, "//div[text()='Post shared']")))
                        break
                    except:
                        print('sharing')
                try:
                    close_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@aria-label='Close'])[1]")))
                    time.sleep(1)
                    close_button.click()
                except Exception as e:
                    print(f"error close_button : {e}")
            else:
                print('couldnt make a post')
        else:
            print('we already have a post')
        '''
        time.sleep(3)
        try:
            try:
                edit_profile = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Edit profile']")))
                time.sleep(2)
                edit_profile.click()
            except Exception as e:
                print(f"error edit_profile : {e}")
            try:
                close_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@aria-label='Close'])[1]")))
                time.sleep(8)
                close_button.click()
            except Exception as e:
                print(f"error close_button edit profile : {e}")

            add_bio = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "pepBio")))
            time.sleep(3)
            text = add_bio.get_attribute("value")
            if not text:
                print('adding bio')
                add_bio.clear()
                human_like_typing(bio_, add_bio)
                add_bio.send_keys('a')
                add_bio.send_keys(Keys.BACKSPACE)
                # try:
            #     any_click= WebDriverWait(driver, 20).until(
            #     EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Gender']")))
            #     time.sleep(0.1)
            #     any_click.click()
            #     actions = ActionChains(driver)
            #     actions.send_keys(Keys.PAGE_DOWN * 4).perform()
                # except Exception as e :
            #     print(e)
                try:
                    submit_bio = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Submit')]")))
                    time.sleep(2)
                    submit_bio.click()
                except Exception as e:
                    print(f"error submit_bio : {e}")
            else:
                print('we aleady have a bio')
        except Exception as e:
            print(e)
            print('error in updating the bio')
        print('finished updating this profile ')
        time.sleep(10)

    def worm_profile(driver, email, go_to_posts=True ,go_to_reels=False):
        if go_to_posts:
            try:
                print('directing to the explore ')
                explore_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[name()='svg' and @aria-label='Explore']")))
                time.sleep(1)
                explore_button.click()
            except Exception as e:
                print(f"error in directing to explore : {e}")
                driver.get('https://www.instagram.com/explore/')
                print('directed using link ')
            try:
                print('choosing any reel')
                posts__ = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//a[@role='link'])[1]")))
                time.sleep(5)
                posts = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[@role='link']")))
                i = 1
                random_num_of_posts = random.randint(3, 9)
                print(f'will serve on {random_num_of_posts} Posts  ')
                for post in posts:
                    if i >= random_num_of_posts:
                        print(f'served {random_num_of_posts} posts')
                        break
                    time.sleep(1)
                    print('going throw posts ')
                    post.click()
                    try:
                        print('like the post')
                        like_the_post = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "(//*[name()='svg' and @aria-label='Like'])[1]/ancestor::div[@role='button']")))
                        time.sleep(3)
                        random_like = random.choice([True, False])
                        if random_like:
                            print('like')
                            driver.execute_script(
                                "arguments[0].click();", like_the_post)
                        else:
                            print('dont like ')
                        random_num_of_scroll = random.randint(3, 9)
                        for A in range(random_num_of_scroll):
                            body = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '//body')))
                            if A % 2 == 0:
                                body.send_keys(Keys.ARROW_RIGHT)
                                time.sleep(1)
                            A += 1
                    except Exception as e:
                        print(f"error in like post : {e}")
                    # random_comment = random.choice([True, False])
                    random_comment = False
                    if random_comment:
                        try:
                            print('getting comments')
                            comments = WebDriverWait(driver, 7).until(
                                EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, '_ap3a') and contains(@class, '_aaco')]")))
                            comments_scraped = []
                            for comment in comments:
                                comments_scraped.append(comment.text)
                            if comments_scraped:
                                comment_to_put = random.choice(
                                    comments_scraped)
                                print(comment_to_put)
                                while True:
                                    try:
                                        print('putting the comment')
                                        posting_the_comment = WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.XPATH, "(//textarea[@aria-label='Add a comment…'])[1]")))
                                        time.sleep(3)
                                        posting_the_comment.clear()
                                        human_like_typing(
                                            comment_to_put, posting_the_comment)
                                        posting_the_comment.send_keys(
                                            Keys.ENTER)
                                        time.sleep(3)
                                        print('comment posted successfully')
                                        break
                                    except Exception as e:
                                        print(f"error in putting the comment :")
                                    except TimeoutException:
                                        print('no comment filed')
                                        break
                            else:
                                print('no comments ')
                        except Exception as e:
                            print(f"there is no comments  : {e}")
                    else:
                        print('wont make a comment')

                    body = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//body')))
                    body.send_keys(Keys.ESCAPE)
                    print('post cloesd')
                    sleep_duration = random.randint(5, 30)
                    print(f"Sleeping for {sleep_duration} seconds")
                    time.sleep(sleep_duration)
                    i += 1
            except Exception as e:
                print(f"error in choosing posts : {e}")
            time.sleep(10)
        if go_to_reels:
            try:
                print('directing to reels ')
                reels_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[name()='svg' and @aria-label='Reels']")))
                time.sleep(1)
                reels_button.click()
            except Exception as e:
                print(f"error in directing to reels : {e}")
                driver.get('https://www.instagram.com/reels/')
                print('directed using link ')
            try:
                time.sleep(15)
                print('like the reels')
                for i in range(2):
                    like_the_reels = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "(//*[name()='svg' and @aria-label='Like'])/ancestor::div[@role='button']")))
                    time.sleep(3)
                    random_like = random.choice([True, False])
                    liked = False
                    list_data=[]
                    for like_the_reel in like_the_reels:
                        if like_the_reel not in list_data:
                            if random_like:
                                if not liked:
                                    print('like')
                                    driver.execute_script(
                                        "arguments[0].click();", like_the_reel)
                                    liked = True
                            driver.execute_script(
                                "arguments[0].scrollIntoView(true);", like_the_reel)
                            time.sleep(3)
                            list_data.append(like_the_reel)

                    else:
                        print('dont like ')
                    random_num_of_scroll = random.randint(3, 9)
                    for A in range(random_num_of_scroll):
                        body = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//body')))
                        if A % 2 == 0:
                            body.send_keys(Keys.ARROW_RIGHT)
                            time.sleep(1)
                        A += 1
            except Exception as e:
                print(f"error in like post : {e}")

            time.sleep(10)

    def follow_each_other_func(accs_list):
     if accs_list:
        print("the day is in excute processed successfully.")
        i = 0
        if email in accs_list :
            accs_list.remove(email)
        for me,user_id in enumerate(accs_list):
            # user_id = user_info['Username']
            if user_id :
                try:
                    search_button = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@aria-label='Search'])[1]")))
                    try:
                        search_button.click()
                    except:
                        driver.refresh()
                        search_button = WebDriverWait(driver, 40).until(
                            EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@aria-label='Search'])[1]")))
                        if search_button:
                            time.sleep(3)
                            search_button.click()
                    print("clicked")
                    time.sleep(2)
                    search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[placeholder='Search']")))
                    human_like_typing(text=user_id, input_field=search_box)
                    time.sleep(3)
                    try:
                        choose_the_id = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located(
                                (By.XPATH, f"//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj' and text()='{user_id}']"))
                        )
                        try:
                            choose_the_id.click()
                            print('clicked id')
                            time.sleep(2)
                        except:
                            print(
                                'Stale Element Reference Exception - retrying click')
                        time.sleep(2)
                        try:
                            follow_account = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "(//div[@class='_ap3a _aaco _aacw _aad6 _aade'])[1]")))
                            if follow_account:
                                time.sleep(2)
                                follow_account.click()
                                print('followed the account')
                        except Exception as e:
                            print(f"error in follow_account {e}")

                        i += 1
                        if me < len(accs_list) - 1:
                            delay_between_messages = generate_delay(1, 3)
                            print(delay_between_messages)
                            time.sleep(delay_between_messages)
                        else:
                            time.sleep(7)

                        if i % 10 == 0:
                            print(f"\nPausing after {i} messages...\n")
                            pause_duration = generate_delay(10, 20)
                            print(pause_duration)
                            time.sleep(pause_duration)

                    except TimeoutException:
                        print("Timed out waiting for the icon to be present.")
                        driver.get(f'https://www.instagram.com/{user_id}/')
                        a7a=False
                        try:
                            follow_account = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "(//div[@class='_ap3a _aaco _aacw _aad6 _aade'])[1]")))
                            if follow_account:
                                time.sleep(2)
                                follow_account.click()
                                a7a = True
                                print('followed the account')
                        except Exception as e:
                            print(f"error in follow_account {e}")
                        if a7a :
                            i += 1
                            if me < len(accs_list) - 1:
                                delay_between_messages = generate_delay(1, 3)
                                print(delay_between_messages)
                                time.sleep(delay_between_messages)
                            else:
                                time.sleep(7)

                            if i % 10 == 0:
                                print(f"\nPausing after {i} messages...\n")
                                pause_duration = generate_delay(10, 20)
                                print(pause_duration)
                                time.sleep(pause_duration)

                except TimeoutException:
                    print('time out happened')
            else:
                print(f'we already follow this account {user_id}')

        if driver is not None:
            driver.quit()
        print('finished')
     else:
        print("No data accounts found for today.")

    driver = get_webdriver_with_proxy()
    driver.get("https://www.instagram.com/")
    try:
        file_name = f"{email}.txt"
        file_path = os.path.join("cookies", file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("[]")
        time.sleep(1)
        load_cookies(driver, file_name)
        driver.get("https://www.instagram.com/")
        skip = False
        try:
            make_sure_we_logged_in = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "(//*[name()='svg'][@aria-label='Home'])[1]")
                )
            )
            if make_sure_we_logged_in:
                print("we already logged in before")
        except Exception as e:
            print("we need to login")
            if not login_to_insta(email, password, bot_name, EMAIL_ACCOUNT, EMAIL_PASSWORD):
                skip = True
                csv_file_path = f"needs/bot_{bot_name}_.csv"
                value_to_remove_fun(email, csv_file_path)
                from tkinter import messagebox
                messagebox.showinfo("warning", f"deleted this account {
                                    email} its not valid")

        if not skip:
            if not make_sure_we_logged_in:
                time.sleep(1)
                load_cookies(driver, file_name)
                driver.refresh()
            if update_the_profile:
                try:
                    update_profile(driver, email)
                except Exception as e:
                    print(f"Exception occurred: {e}")
            if worm_the_profile:
                try:
                    worm_profile(driver, email)
                except Exception as e:
                    print(f"Exception occurred: {e}")
            if follow_each_other:
               try:
                follow_each_other_func(accs_list)
               except Exception as e :
                   print(e)

    finally:
        if driver is not None:
            driver.quit()


# Main_action('slsnesjos', 'DSMLJwttfb169862', 'bot_sbUESBYd_1',
#             'ksgsybaukm@rambler.ru', '5521268OZB4Zn', False, False,True,data)
# # yore.o9320,ohXp894t249K2Y5Aa,clyxtgmofh@rambler.ru,48788147WWpMl
