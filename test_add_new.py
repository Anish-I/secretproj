import os
import zipfile
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
bot_name='medo'
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
        co.add_argument("--force-dark-mode=false")
        co.add_argument("--lang=en")
        co.add_argument(f"--user-data-dir={temp_dir}")
        co.add_extension(pluginfile)
           # Add this to force the browser to light mode
        prefs = {"profile.default_content_setting_values.cookies": 2}
        co.add_experimental_option("prefs", prefs)
        
        # Launch Chrome with white mode enforced
        co.add_argument('--blink-settings=darkMode=0')
        driver = webdriver.Chrome(options=co)
        driver.get("https://www.google.com/")
        # Inject JS to force light mode
        # js = """
        # var style = document.createElement('style');
        # style.innerHTML = '@media (prefers-color-scheme: dark) { html { filter: invert(100%) hue-rotate(180deg); } }';
        # document.head.appendChild(style);
        # """
        # driver.execute_script(js)
        driver.refresh()
        return driver

driver=get_webdriver_with_proxy()
time.sleep(1000)