# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller import __main__ as pyi_main

args = [
    '--onefile',
       '--add-data=The_gui.py:.',  # Include The_gui.py in the root
       '--add-data=captcha_solver_selen.py:.',  # Include captcha_solver_selen.py in the root
       '--add-data=get_customers.py:.',  # Include captcha_solver_selen.py in the root
       '--add-data=login_handling_for_tester.py:.',  # Include follow_unfollow.py in the root
       '--add-data=login_handling.py:.',  # Include login_handling.py in the root
       '--add-data=process_the_xlsx.py:.',  # Include login_handling.py in the root
       '--add-data=start1_with_last_mod.py:.',
       '--add-data=needs:needs',  # Include the 'static' directory
       '--add-data=extentions:extentions',  # Include the 'templates' directory
       '--add-data=cookies:cookies',
       '--add-data=logo.png:.',  # Include the picture in the root
    '--hidden-import', ','.join(collect_submodules('.')),  # Collect hidden imports
    '--noconsole',  # Set console to False
    '--icon=logo.png',  # Set the icon (assuming it's in .ico format)
    '--name=INSTA Multi bots',  # Set the app name to YourAppName
    'The_gui.py'  # Set the main script to daily_checker.py
]


pyi_main.run(args)
