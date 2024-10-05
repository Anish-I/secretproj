import webbrowser
import tkinter
import re
import os
import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
# Ensure you have this module
from login_handlingscraper import load_cookies, login_to_insta
# from Dm_seder import kosom_da_script
import threading 
from start1_with_last_mod import worker_1
# from add___task import create_task
import shutil
# from get_user_names import get_cutomers
import string
import random
from threading import Thread
from get_customers import main_scraper
from login_handling_for_tester import login_to_insta2
import time
import sys


sub_user = 'default_user'  # Change this based on your needs


if not os.path.exists('cookies'):
        os.makedirs('cookies')
        # create_task()


# Functions from the first script
def save_username_and_name_from_file(file_path):
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8', errors='replace') as csvfile:
            reader = csv.reader(csvfile)
            try:
                next(reader)  # Skip the header
            except StopIteration:
                pass  # Handle the case where the file is empty
            for row in reader:
                data.append(row[:2])  # Save only the first 2 columns
    except FileNotFoundError:
        pass
  

    save_introws_list_csv(data)


def save_introws_list_csv(data_comming):
    bot_name=get_user_name_and_pass()
    filename = f"needs/users_to_reach_{bot_name}_.csv"
    data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row[:2])  # Save only the first 2 columns
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for sub_data in data_comming:
            if sub_data not in data:
                writer.writerow(sub_data)


def users_data_func():
    folder_path = "needs"
    for file_name in os.listdir(folder_path):
        bot_name=get_user_name_and_pass()
        if file_name.startswith(f"users_to_reach_{bot_name}_"):
            return True
    return False


def get_all_uses_data():
    users_data = []
    if users_data_func():
        folder_path = "needs"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"users_to_reach_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    try:
                        next(csv_reader)
                    except StopIteration:
                        pass
                    for row in csv_reader:
                        # Get only the first 2 columns
                        users_data.append(row[:2])

    return users_data


def delete_all_users_data():
    if users_data_func():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"users_to_reach_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                deleted = True
        return deleted
    return False


def delete_user_from_csv(intro):
    if users_data_func():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"users_to_reach_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    if row[:2] == intro:
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False


def add_users_from_file():
    bot_name=get_user_name_and_pass()
    if bot_name:
        messagebox.showwarning("warning","the first 2 columns should be username,name")
        file_path = filedialog.askopenfilename(
        title="Select CSV file", filetypes=(("CSV files", "*.csv"),))
        if file_path:
        
         save_username_and_name_from_file(file_path)
         messagebox.showinfo("Success", "Data added from file")
        else:
             messagebox.showerror("Error", "No file selected")
    else:
       messagebox.showerror("Error", "No user selected")


def show_current_data():
 
    bot_name=get_user_name_and_pass()
    if bot_name: 
       all_users = get_all_uses_data()
       if all_users:
        show_data_window = tk.Toplevel(GUI)
        show_data_window.title("Current to text people")

        # Create a Treeview
        tree = ttk.Treeview(show_data_window, columns=(
            'Username', 'Name'), show='headings')
        tree.heading('Username', text='Username')
        tree.heading('Name', text='Name')
        tree.column('Username', width=150)
        tree.column('Name', width=150)

        # Add data to the Treeview
        for intro in all_users:
            tree.insert('', tk.END, values=intro)

        # Add a Scrollbar
        scrollbar = ttk.Scrollbar(
            show_data_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        # Place the Treeview and Scrollbar
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        show_data_window.grid_rowconfigure(0, weight=1)
        show_data_window.grid_columnconfigure(0, weight=1)
        
        # Add a label to show the number of accounts found
        num_accounts_label5 = tk.Label(show_data_window, text=f"Number of users found: {len(all_users)}")
        num_accounts_label5.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        # Add delete buttons
        def delete_selected():
            selected_items = tree.selection()
            for selected_item in selected_items:
                item_values = tree.item(selected_item)['values']
                if delete_user_from_csv(item_values):
                    tree.delete(selected_item)
                    num_accounts_label5.config(text=f"Number of users found: {len(tree.get_children())}")
                    show_number_of_To_message()

        delete_button__ = tk.Button(
            show_data_window, text="Delete Selected", command=delete_selected)
        delete_button__.grid(row=2, column=0, padx=5, pady=5)
       else:
            messagebox.showerror("Error", "No users found")

    else:
         messagebox.showerror("Error", "No user selected")


def delete_all_usesrs_():
    if delete_all_users_data():
        messagebox.showinfo("Success", "All users deleted")
    else:
        messagebox.showerror("Error", "No users to delete")


# functions from the sub second script
def save_username_only_from_file(file_path):
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                next(reader)  # Skip the header
            except StopIteration:
                pass  # Handle the case where the file is empty
            for row in reader:
                data.append([row[0]])  # Save only the first column (username)
    except FileNotFoundError:
        pass

    save_user_names_list_csv(data)


def save_user_names_list_csv(data_coming):
    bot_name=get_user_name_and_pass()
    filename = f"needs/texted_people_{bot_name}_.csv"
    data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append([row[0]])  # Save only the first column (username)
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for sub_data in data_coming:
            if sub_data not in data:
                writer.writerow(sub_data)


def users_data_func___a():
    folder_path = "needs"
    for file_name in os.listdir(folder_path):
        bot_name=get_user_name_and_pass()
        if file_name.startswith(f"texted_people_{bot_name}_"):
            return True
    return False


def get_all_uses_data___():
    users_data = []
    if users_data_func___a():
        folder_path = "needs"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"texted_people_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    try:
                        next(csv_reader)
                    except :
                        pass
                    for row in csv_reader:
                        # Get only the first column (username)
                        users_data.append([row[0]])

    return users_data


def delete_user_from_csv____a(intro):
    if users_data_func___a():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"texted_people_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    # Check only the first column (username)
                    if row[0] == intro[0]:
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False


def add_users_from_file___():
    bot_name=get_user_name_and_pass()
    if bot_name:
        messagebox.showwarning("warning","the first column should be username ")
        file_path = filedialog.askopenfilename(
        title="Select CSV file", filetypes=(("CSV files", "*.csv"),))
        if file_path:
   
          save_username_only_from_file(file_path)
          messagebox.showinfo("Success", "Data added from file")
        else:
             messagebox.showerror("Error", "No file selected")
    else:
      messagebox.showerror("Error", "No user selected")  


def show_current_data___a():
    bot_name=get_user_name_and_pass()
    if bot_name:
      all_users = get_all_uses_data___()
      if all_users:
        show_data_window2 = tk.Toplevel(GUI)
        show_data_window2.title("Current users")

        # Create a Treeview
        tree = ttk.Treeview(show_data_window2, columns=(
            'Username',), show='headings')
        tree.heading('Username', text='Username')
        tree.column('Username', width=300)

        # Add data to the Treeview
        for intro in all_users:
            tree.insert('', tk.END, values=intro)

        # Add a Scrollbar
        scrollbar = ttk.Scrollbar(
            show_data_window2, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        # Place the Treeview and Scrollbar
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        show_data_window2.grid_rowconfigure(0, weight=1)
        show_data_window2.grid_columnconfigure(0, weight=1)
        
         # Add a label to show the number of accounts found
        num_accounts_label2 = tk.Label(show_data_window2, text=f"Number of users found: {len(all_users)}")
        num_accounts_label2.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        # Add delete buttons
        def delete_selected():
            selected_items = tree.selection()
            for selected_item in selected_items:
                item_values = tree.item(selected_item)['values']
                if delete_user_from_csv____a(item_values):
                    tree.delete(selected_item)
                    num_accounts_label2.config(text=f"Number of users found: {len(tree.get_children())}")
                    show_number_of_To_history()


        delete_button___ = tk.Button(
            show_data_window2, text="Delete Selected", command=delete_selected)
        delete_button___.grid(row=2, column=0, padx=5, pady=5)
      else:
        messagebox.showerror("Error", "No users found")
    else:
        messagebox.showerror("Error", "No user selected")



def delete_all_users_data___a():
    if users_data_func___a():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"texted_people_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                deleted = True
        return deleted
    return False


def delete_intro_and_refresh__(window, intro):
    if delete_user_from_csv____a(intro):
        messagebox.showinfo("Success", f"Intro '{intro[0]}' deleted")
        window.destroy()
        show_current_data___a()
    else:
        messagebox.showerror("Error", f"Intro '{intro[0]}' not found")


def delete_all_usesrs_____a():
    if delete_all_users_data___a():
        messagebox.showinfo("Success", "All users deleted")
    else:
        messagebox.showerror("Error", "No users to delete")


# Functions from the second script
def users_data_func___a_a():
    folder_path = "needs"
    for file_name in os.listdir(folder_path):
        if file_name.startswith("Dm_emails_all"):
            return True
    return False


def get_all_users_data___aa1():
    users_data = []
    if users_data_func___a_a():
        folder_path = "needs"
        for file_name in os.listdir(folder_path):
            if file_name.startswith("Dm_emails_all"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        # Get the first two columns (username and password)
                        users_data.append([row[0]])
    return users_data


def delete_user_from_csv____a_a1(intro):
    if users_data_func___a_a():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            if file_name.startswith(f"Dm_emails_all"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    if row[0] == intro[0]:  # Check the first column (username)
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False


def delete_all_users_data___a_a():
    if users_data_func___a_a():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            if file_name.startswith(f"Dm_emails_all"):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                deleted = True
        return deleted
    return False


def refresh_data_a1():
    users = get_all_users_data___aa1()
    combo['values'] = [f"{user[0]} " for user in users]
    # combo['values'] = [f"  {user[0]}" for user in users]
    if users:
        combo.current(0)  # Set the first item as selected
    else:
        combo.set('')

def delete_selected_a1():
    selected_item = combo.get()
    if selected_item:
        bot_name = selected_item.split(" ")[0]
        if delete_user_from_csv____a_a1([bot_name]):
            refresh_data_a1()
            refresh_username()
            use_selected_1()


def use_selected_1():
    selected_item = combo.get()
    print(selected_item)
    if selected_item:
        bot_name = selected_item.split(" ")[0]
        # with open("needs/Dm_emails.csv", mode='w', newline='', encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     # writer.writerow(["username", "password"])  # Write the header
        #     writer.writerow([username, password])

        refresh_username()
        messagebox.showinfo("Success", "Selected data saved to data.csv")

def bot_data_found():
    folder_path = "needs"
    for file_name in os.listdir(folder_path):
        bot_name=get_user_name_and_pass()
        if file_name.startswith(f"bot_{bot_name}_"):
            return True
    return False

def get_all_bot_data():
    users_data = []
    if bot_data_found():
        folder_path = "needs"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"bot_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        # Get only the first 2 columns
                        users_data.append(row[:5])

    return users_data

def delete_user_from_bot_data(intro):
    print(intro)
    if bot_data_found():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"bot_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    if row[:2] == intro:
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False

def show_accounts_in_the_bot():
    bot_name = get_user_name_and_pass()
    if bot_name:
        all_users = get_all_bot_data()
        if all_users:
            show_data_window_for_bot = tk.Toplevel(GUI)
            show_data_window_for_bot.title(f"Current Bot users {bot_name}")

            # Create a Treeview with an extra column for the login status
            tree = ttk.Treeview(show_data_window_for_bot, columns=('Username', 'Password', 'Login Status'), show='headings')
            tree.heading('Username', text='Username')
            tree.heading('Password', text='Password')
            tree.heading('Login Status', text='Login Status')
            tree.column('Username', width=150)
            tree.column('Password', width=150)
            tree.column('Login Status', width=100)

            # Add data to the Treeview
            for intro in all_users:
                username = intro[0]
                password = intro[1]
                
                # Check if the 5th value (login status) exists
                if len(intro) > 4: 
                    status = intro[4]  # 5th value (Yes or No)
                    login_status = "Not Logged" if status == "Yes" else "Logged"
                else:
                    login_status = "Not Logged"  # Default to "Not Logged" if 5th value is not present

                tree.insert('', tk.END, values=(username, password, login_status))

            # Add a Scrollbar
            scrollbar = ttk.Scrollbar(show_data_window_for_bot, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)

            # Place the Treeview and Scrollbar
            tree.grid(row=0, column=0, sticky='nsew')
            scrollbar.grid(row=0, column=1, sticky='ns')

            show_data_window_for_bot.grid_rowconfigure(0, weight=1)
            show_data_window_for_bot.grid_columnconfigure(0, weight=1)

            # Add a label to show the number of accounts found
            num_accounts_label = tk.Label(show_data_window_for_bot, text=f"Number of accounts found: {len(all_users)}")
            num_accounts_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            # Add delete buttons
            def delete_selected():
                selected_items = tree.selection()
                for selected_item in selected_items:
                    item_values = tree.item(selected_item)['values']
                    item_values.pop()
                    if delete_user_from_bot_data(item_values):
                        tree.delete(selected_item)
                        num_accounts_label.config(text=f"Number of accounts found: {len(tree.get_children())}")
                        show_number_of_accounts_in_bot()

            delete_button____ = tk.Button(show_data_window_for_bot, text="Delete Selected", command=delete_selected)
            delete_button____.grid(row=2, column=0, padx=5, pady=5)

        else:
            messagebox.showerror("Error", "No user found")
    else:
        messagebox.showerror("Error", "No bot selected")




def save_test_account_data_aa(file_path,bot_name):
    with open(f'needs/Dm_emails_all.csv', mode='a', newline='', encoding='utf-8') as file:
     writer = csv.writer(file)
     writer.writerow([bot_name])
    
    data_comming = []
    try:
        with open(file_path, 'r', encoding='utf-8') as txtfile:
            for line in txtfile:
                line_data = line.strip().split(':')  # Split by colon
                if len(line_data) == 4:  # Ensure there are exactly 4 parts
                    data_comming.append(line_data)
    except FileNotFoundError:
        pass

    filename = f"needs/bot_{bot_name}_.csv"
    data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row[:4])  # Save only the first 4 columns
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for sub_data in data_comming:
            if sub_data not in data:
                writer.writerow(sub_data)
    refresh_data_a1()  # Update the accounts display

def generate_random_string(length=8):
    letters = string.ascii_letters  # This includes both uppercase and lowercase letters
    return ''.join(random.choice(letters) for i in range(length))

def add_new_bot():
        users_data=get_all_users_data___aa1()
        bot_name=f"bot_{generate_random_string()}_{len(users_data)+1}"
        messagebox.showwarning("warning","the first 2 columns should be username,name")
        file_path = filedialog.askopenfilename(
        title="Select Text File", filetypes=(("Text files", "*.txt"),))
        if file_path:
         save_test_account_data_aa(file_path,bot_name)
         messagebox.showinfo("Success", "Data added from file")
        else:
             messagebox.showerror("Error", "No file selected")


# Functions from the first script
def add_proxy():
    # Gather data from entry fields
    proxy_host = entry_host.get()
    proxy_port = entry_port.get()
    user_name = entry_user.get()
    password = entry_password.get()

    # Validate if all fields are filled
    if proxy_host == '' or proxy_port == '' or user_name == '' or password == '':
        messagebox.showerror('Error', 'Please fill in all fields')
        return

    # Format the data
    proxy_data = f"{proxy_host},{proxy_port},{user_name},{password}\n"
    
    bot_name=get_user_name_and_pass()
    if bot_name:
     # Append data to the file
     with open(f'needs/proxy_{bot_name}_.txt', 'w', encoding='utf-8') as file:
        file.write(proxy_data)

     # Set placeholder text
     entry_host.delete(0, tk.END)
     entry_host.insert(0, proxy_host)

     entry_port.delete(0, tk.END)
     entry_port.insert(0, proxy_port)

     entry_user.delete(0, tk.END)
     entry_user.insert(0, user_name)

     entry_password.delete(0, tk.END)
     entry_password.insert(0, password)

     messagebox.showinfo('Success', 'Proxy data added successfully')
    else:
     messagebox.showerror("Error", "No user selected")


# font_style = ('Helvetica', 12)
# # Create the main window
# root = tk.Tk()
# root.title("Instagram Test Account Manager")
# root.option_add('*Font', font_style)  # Apply global font style


def Get_HWND_DPI(window_handle):
    # To detect high DPI displays and avoid need to set Windows compatibility flags
    import os
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass  # this will fail on Windows Server and maybe early Windows
        DPI100pc = 96  # DPI 96 is 100% scaling
        DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(
            winH, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(
                monitorhandle, DPI_type, pointer(X), pointer(Y))
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1  # What to do for other OSs?


def TkGeometryScale(s, cvtfunc):
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G


def MakeTkDPIAware(TKGUI):
    TKGUI.DPI_X, TKGUI.DPI_Y, TKGUI.DPI_scaling = Get_HWND_DPI(
        TKGUI.winfo_id())
    TKGUI.TkScale = lambda v: int(float(v) * TKGUI.DPI_scaling)
    TKGUI.TkGeometryScale = lambda s: TkGeometryScale(s, TKGUI.TkScale)

# Function to read the username from the CSV file


def get_username_from_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:
                return row[0]  # Assuming the first column is the username
    return "No bot name Found"

# Function to update the username label
def refresh_username():
    selected_item = combo.get()
    bot_name=''
    if selected_item:
        bot_name = selected_item.split(" ")[0]
    if not bot_name:
        bot_name ='No bot_name Found'
    refresh_data_list('outro')
    refresh_data_list('body')
    refresh_data_list('intro')
    load_data_numeric()
    load_data_proxy() 
    load_saved_settings()
    load_settings_for_scraper_type()
    show_current_data_for_scraper()
    load_data_proxy_scraper()
    show_number_of_accounts_in_bot()
    show_number_of_To_history()
    show_number_of_To_message()
    load_data_of_sleep_test(entry_min_minute2,'main')
    load_data_of_sleep_test(entry_min_minute2_scrape,'scraper')
    load_link()
    refresh_data_a1_scraper()
    # user_nam = get_bot_name_from_csv('needs/Dm_emails.csv')
    GUI.title(f"INSTA DM  ----->>> {f"{bot_name}"}")

def get_user_name_and_pass():
    selected_item = combo.get()
    bot_name=''
    if selected_item:
        bot_name = selected_item.split(" ")[0]
    return bot_name
# Example use:


GUI = tkinter.Tk()
GUI.title("INSTA DM")
GUI.resizable(False, False)


def open_website():
    webbrowser.open("https://t.me/Bek_El_Ghandour")


logo = tk.PhotoImage(file="extentions/logo_1.png")
GUI.iconphoto(False, logo)
link_label = tk.Label(GUI, text="Developed by Ghandour",
                      fg="blue", cursor="hand2", font=("Arial", 8))
link_label.bind("<Button-1>", lambda e: open_website())
link_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)



MakeTkDPIAware(GUI)  # Sets the windows flag + gets adds .DPI_scaling property
GUI.geometry(GUI.TkGeometryScale("1100x840+200+100"))
gray = "#cccccc"
DemoFrame = tkinter.Frame(GUI, width=GUI.TkScale(
    1080), height=GUI.TkScale(780), background=gray)
DemoFrame.place(x=GUI.TkScale(10), y=GUI.TkScale(10))
DemoFrame.pack_propagate(False)

from tkinter import scrolledtext

class PrintLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        if self.text_widget is not None and self.text_widget.winfo_exists():
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)

    def flush(self):
        pass

# Save the original stdout and stderr
original_stdout = sys.stdout
original_stderr = sys.stderr

debug_window = None

def open_debug_window():
    global debug_window, print_logger
    if debug_window is None or not debug_window.winfo_exists():
        debug_window = tk.Toplevel(GUI)
        debug_window.title("Debug Window")
        
        # Create a scrolled text widget
        text_area = scrolledtext.ScrolledText(debug_window, wrap=tk.WORD, height=20)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Redirect stdout and stderr to the text widget
        print_logger = PrintLogger(text_area)
        sys.stdout = print_logger
        sys.stderr = print_logger
        
        def on_closing():
            global debug_window, print_logger
            # Restore the original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            debug_window.destroy()
            debug_window = None
            print_logger = None

        debug_window.protocol("WM_DELETE_WINDOW", on_closing)



# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(DemoFrame)

# Create the Account Management tab
account_frame = ttk.Frame(notebook)
notebook.add(account_frame, text="Account Management")

# Create the DM Sending tab
dm_frame = ttk.Frame(notebook)
notebook.add(dm_frame, text="DM Sending")

# Create the DM Sending tab
Scraper_frame = ttk.Frame(notebook)
notebook.add(Scraper_frame, text="The Scraper")

# Pack the Notebook
notebook.pack(expand=True, fill='both')

# Define a style for frames
frame_style = {'highlightthickness': 1, 'bd': 2, 'relief': tk.RIDGE}

# Create frames for each section
frame1 = tk.Frame(account_frame, padx=10, pady=10, **frame_style)
frame1.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame2 = tk.Frame(account_frame, padx=10, pady=10, **frame_style)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create frame for proxy management
frame3 = tk.Frame(account_frame, padx=10, pady=10, **frame_style)
frame3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Widgets for frame1 (first script)
# tk.Label(frame1, text="Data Manager", font=("Helvetica", 16)).pack(pady=10)

# add_button = tk.Button(frame1, text="Add data", command=add_users_from_file)
# add_button.pack(pady=5)

# show_button = tk.Button(frame1, text="Show Current Data", command=show_current_data)
# show_button.pack(pady=5)

# delete_all_button = tk.Button(frame1, text="Delete All data", command=delete_all_usesrs_)
# delete_all_button.pack(pady=5)


# Create a frame for History Data
sub_frame0 = tk.Frame(frame1, relief=tk.SUNKEN, borderwidth=2)
sub_frame0.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Label for History Data
label1 = tk.Label(sub_frame0, text="History Data",
                  font=('Helvetica', 12, 'bold'))
label1.pack(pady=10)

# Buttons for History Data
add_button1 = tk.Button(sub_frame0, text="Add history data",
                        command=add_users_from_file___)
add_button1.pack(pady=5)

show_button1 = tk.Button(
    sub_frame0, text="Show History Data", command=show_current_data___a)
show_button1.pack(pady=5)

delete_all_button1 = tk.Button(
    sub_frame0, text="Delete All History data", command=delete_all_usesrs_____a)
delete_all_button1.pack(pady=5)



num_accounts_label5 = None
num_accounts_label3=None
num_accounts_label6=None
def show_number_of_To_history():
 user_name_he=get_user_name_and_pass()
 global num_accounts_label3
 try:
     num_accounts_label3.destroy()
 except:
     pass
 if user_name_he: 
  all_users = get_all_uses_data___()
  if all_users:
            if num_accounts_label3 is None:
                # Create the label if it doesn't exist
                num_accounts_label3 = tk.Label(sub_frame0, text=f"Number of users found: {len(all_users)}")
                num_accounts_label3.pack(pady=5)
            else:
                # Update the text of the existing label
                num_accounts_label3.destroy()
                num_accounts_label3 = tk.Label(sub_frame0, text=f"Number of users found: {len(all_users)}")
                num_accounts_label3.pack(pady=5)
    

      

def check_bot_foubnd():
    folder_path = "needs"
    for file_name in os.listdir(folder_path):
        bot_name=get_user_name_and_pass()
        if file_name.startswith(f"bot_{bot_name}_"):
            return True
    return False

def get_all_accounts_in_bots():
    users_data = []
    if check_bot_foubnd():
        folder_path = "needs"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"bot_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        # Get only the first column (username)
                        users_data.append([row[0]])

    return users_data

def show_number_of_accounts_in_bot():
 user_name_he=get_user_name_and_pass()
 global num_accounts_label6
 try:
                     num_accounts_label6.destroy()
 except :
     pass
 if user_name_he: 
  all_users = get_all_accounts_in_bots()
  if all_users:
            if num_accounts_label6 is None:
                # Create the label if it doesn't exist
                num_accounts_label6 = tk.Label(fram_e, text=f"Number of accounts found : {len(all_users)}")
                num_accounts_label6.pack(pady=5)
            else:
                num_accounts_label6.destroy()
                num_accounts_label6 = tk.Label(fram_e, text=f"Number of accounts found : {len(all_users)}")
                num_accounts_label6.pack(pady=5)
# Create a frame for Data Manager
subframe_0_1 = tk.Frame(frame1, relief=tk.SUNKEN, borderwidth=2)
subframe_0_1.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Label for Data Manager
label2 = tk.Label(subframe_0_1, text="To Message",
                  font=('Helvetica', 12, 'bold'))
label2.pack(pady=10)

# Buttons for Data Manager
add_button2 = tk.Button(subframe_0_1, text="Add data",
                        command=add_users_from_file)
add_button2.pack(pady=5)

show_button2 = tk.Button(
    subframe_0_1, text="Show Current Data", command=show_current_data)
show_button2.pack(pady=5)

delete_all_button2 = tk.Button(
    subframe_0_1, text="Delete All data", command=delete_all_usesrs_)
delete_all_button2.pack(pady=5)


def show_number_of_To_message():
 user_name_he=get_user_name_and_pass()
 global num_accounts_label5

 try:
           num_accounts_label5.destroy()
 except:
     pass
 if user_name_he: 
  all_users = get_all_uses_data()
  if all_users:
    if num_accounts_label5 is None:
        # Create the label if it doesn't exist
        num_accounts_label5 = tk.Label(subframe_0_1, text=f"Number of users found: {len(all_users)}")
        num_accounts_label5.pack(pady=5)
    else:
        # Destroy the existing label and create a new one
        num_accounts_label5.destroy()
        num_accounts_label5 = tk.Label(subframe_0_1, text=f"Number of users found: {len(all_users)}")
        num_accounts_label5.pack(pady=5)
     


# Widgets for frame2 (second script)


fram_e = tk.Frame(frame2)
fram_e.pack(padx=10, pady=10)


add_button = tk.Button(fram_e, text="Add NEW BOT", command=add_new_bot)
add_button.pack(pady=5)

show_bot_accounts = tk.Button(fram_e, text="Show Bot Acounts", command=show_accounts_in_the_bot)
show_bot_accounts.pack(pady=5)

# Create a Combobox
user_data = tk.StringVar()
combo = ttk.Combobox(fram_e, textvariable=user_data,
                     state='readonly', width=30)
combo.pack(pady=10)

# Create a fram_e for the delete and use buttons
button_frame = tk.Frame(fram_e)
button_frame.pack(pady=5)

# Add delete button
delete_button = tk.Button(
    button_frame, text="Delete Selected", command=delete_selected_a1)
delete_button.grid(row=0, column=0, padx=5)

# Add use button
use_button = tk.Button(button_frame, text="Use Selected",
                       command=use_selected_1)
use_button.grid(row=0, column=1, padx=5)

tester_frame = tk.Frame(fram_e, bd=2, relief='sunken')
tester_frame.pack(pady=5)


# here the class asked for testing the accounts in the bot

class AccountManager:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def change_state(self, user_name):
        # Read the CSV file into a list of lists
        with open(self.csv_file_path, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)  # Read all rows into a list

        # Modify the 'account valid' state for the specified user
        for row in rows:
            if row[0] == user_name:
                row[4] = 'No'

        # Write the modified rows back to the original CSV file
        with open(self.csv_file_path, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)  # Write the modified rows


    def insert_yes(self):
        # Define the file path
        file_path = self.csv_file_path

        # Read the contents of the file
        with open(file_path, 'r', encoding='utf-8') as input_file:
            # Read all lines from the input file
            lines = list(csv.reader(input_file))

        # Open the file for writing (overwrite mode)
        with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
            # Create a CSV writer object
            csv_writer = csv.writer(output_file)
            
            # Iterate over the read lines
            for row in lines:
                # Insert 'Yes' into the third position
                row.insert(4, 'Yes')
                # Write the modified row to the file
                csv_writer.writerow(row)

        print(f"Data has been successfully transformed in {file_path}")

    def value_to_remove_fun(self, value_to_remove):
        removed_rows = []  # List to hold the removed row(s)

        # Read data from the original CSV and filter out the line to remove
        with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as infile:
            csvreader = csv.reader(infile)
            rows = []
            for row in csvreader:
                if row[0] == value_to_remove:
                    removed_rows.append(row)  # Add the row to the removed_rows list
                else:
                    rows.append(row)  # Keep other rows

        # Write the filtered data back to the original CSV file
        with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerows(rows)

        # Append the removed row(s) to the removed_accs.csv file
        if removed_rows:
            with open('removed_accs.csv', 'a', newline='', encoding='utf-8') as removed_file:
                csvwriter = csv.writer(removed_file)
                csvwriter.writerows(removed_rows)

    def test_accounts_we_have(self,use_rambler):
        existing_mails = []
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    existing_mails.append({'email': row[0], 'password': row[1],'inbox_mail':row[2],'inbox_pass':row[3],
                                           'account_valid': row[4]})
        except:
            self.insert_yes()
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    existing_mails.append({'email': row[0], 'password': row[1],'inbox_mail':row[2],'inbox_pass':row[3],
                                           'account_valid': row[4]})

        for email_data in existing_mails:
            email = email_data.get('email')
            password = email_data.get('password')
            inbox_mail=email_data.get('inbox_mail')
            inbox_pass=email_data.get('inbox_pass')
            account_valid = email_data.get('account_valid')

            if account_valid == 'Yes':
                bot_name=get_user_name_and_pass()
                if login_to_insta2(email, password,bot_name,inbox_mail,inbox_pass,use_rambler):
                    print(f'Logged in to account {email}')
                    self.change_state(email)
                else:
                    print('Account invalid\nRemoving from the file')
                    self.value_to_remove_fun(email)
                    show_number_of_accounts_in_bot()
                    print('Done')
                time.sleep(10)

            with open(f'checker_test_{os.path.basename(self.csv_file_path).replace(".csv", "").replace("needs/", "")}_.txt', 'r', encoding='utf-8') as file:
                checker = file.read()
            if checker == "stop":
                break


def start_testing():
    bot_name=get_user_name_and_pass()
    if bot_name:
        add_sleep_to_test_accounts(entry_min_minute2,'main')
        file_name = f'needs/bot_{bot_name}_.csv'
        with open(f'checker_test_{file_name.replace(".csv", "").replace("needs/", "")}_.txt', 'w', encoding='utf-8') as file:
            file.write('Start')
        
        account_manager = AccountManager(file_name)
        # Retrieve the value from the radio buttons
        use_rambler = rambler_var.get()
        print(f"Starting testing with use_rambler={use_rambler}")
        thread = threading.Thread(target=account_manager.test_accounts_we_have, args=(use_rambler,))
        thread.start()
        
def stop_testing_accounts():
    bot_name=get_user_name_and_pass()
    if bot_name:
     file_name=f'needs/bot_{bot_name}_.csv'
     with open(f'checker_test_{file_name.replace('.csv','').replace('needs/','')}_.txt', 'w', encoding='utf-8') as file:
        file.write('stop')
    messagebox.showinfo('Success', 'Stop signal created when bot reach it testing of the accounts will Stop')

from worm_up_accs import Worm_up
import queue

# Queue to store the accounts to process one by one
acc_queue = queue.Queue()

# Global stop flag to control the stopping of threads
stop_flag = False

# Function to process each account (this runs inside each thread)
def process_next_account():
    global stop_flag

    # If stop flag is set, stop processing further accounts
    if stop_flag:
        print("Stopping the worming process...")
        return

    try:
        # Get the next account from the queue
        acc = acc_queue.get_nowait()

        # Extract details from the account
        email = acc['email']
        password = acc['password']
        inbox_mail = acc['inbox_mail']
        inbox_pass = acc['inbox_pass']
        bot_name = acc['bot_name']
        update_the_profile = acc['update_the_profile']
        worm_the_profile = acc['worm_the_profile']
        follow_each_other = acc['follow_each_other']
        accs_list = acc['accs_list']

        # Start the worm-up process for the account
        Worm_up(email, password, bot_name, inbox_mail, inbox_pass, update_the_profile, worm_the_profile, follow_each_other, accs_list)

        # After finishing, signal the queue to continue with the next account
        acc_queue.task_done()

        # If there are more accounts and the stop flag is not set, start the next one
        if not acc_queue.empty() and not stop_flag:
            thread = threading.Thread(target=process_next_account)
            thread.start()

    except queue.Empty:
        print("All accounts have been processed.")


# Worm up the accs one by one using threads sequentially
def start_worming_the_accs():
    global stop_flag
    stop_flag = False  # Reset stop flag when starting

    update_the_profile = update_profile_var.get()
    worm_the_profile = worm_profile_var.get()
    follow_each_other = follow_each_other_var.get()
    bot_name = get_user_name_and_pass()

    if bot_name:
        file_name = f'needs/bot_{bot_name}_.csv'
        existing_mails = []

        # Read the CSV file with the accounts
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                existing_mails.append({'email': row[0], 'password': row[1], 'inbox_mail': row[2], 'inbox_pass': row[3]})

        accs_list = [acc['email'] for acc in existing_mails]

        # Fill the queue with accounts to process
        for acc in existing_mails:
            acc_data = {
                'email': acc['email'],
                'password': acc['password'],
                'inbox_mail': acc['inbox_mail'],
                'inbox_pass': acc['inbox_pass'],
                'bot_name': bot_name,
                'update_the_profile': update_the_profile,
                'worm_the_profile': worm_the_profile,
                'follow_each_other': follow_each_other,
                'accs_list': accs_list
            }
            acc_queue.put(acc_data)

        # Start processing the first account
        if not acc_queue.empty():
            thread = threading.Thread(target=process_next_account)
            thread.start()


# Function to stop the worming process
def stop_worming():
    global stop_flag
    stop_flag = True  # Set the stop flag to True to stop the process
    print("Stop worming process triggered. No new threads will be started.")



# Create radio buttons for "use_rambler" Yes/No option
rambler_var = tk.BooleanVar(value=True)  # Default to Yes (True)
tk.Label(tester_frame, text='Use Rambler?').grid(row=1, column=0, padx=5, pady=5, sticky='e')

yes_button = tk.Radiobutton(tester_frame, text="Yes", variable=rambler_var, value=True)
yes_button.grid(row=1, column=1, sticky='w')

no_button = tk.Radiobutton(tester_frame, text="No", variable=rambler_var, value=False)
no_button.grid(row=1, column=2, sticky='w')

# Create buttons for starting and stopping testing
btn_start = tk.Button(tester_frame, text='Start testing accounts', command=start_testing)
btn_start.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

btn_stop = tk.Button(tester_frame, text='Stop testing accounts', command=stop_testing_accounts)
btn_stop.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')



# for worm up buttons 
# Radio buttons for "update_the_profile" Yes/No option
update_profile_var = tk.BooleanVar(value=True)  # Default to Yes (True)
tk.Label(tester_frame, text='Update the profile?').grid(row=3, column=0, padx=5, pady=5, sticky='e')

yes_update_button = tk.Radiobutton(tester_frame, text="Yes", variable=update_profile_var, value=True)
yes_update_button.grid(row=3, column=1, sticky='w')

no_update_button = tk.Radiobutton(tester_frame, text="No", variable=update_profile_var, value=False)
no_update_button.grid(row=3, column=2, sticky='w')

# Radio buttons for "worm_the_profile" Yes/No option
worm_profile_var = tk.BooleanVar(value=True)  # Default to Yes (True)
tk.Label(tester_frame, text='Worm the profile?').grid(row=4, column=0, padx=5, pady=5, sticky='e')

yes_worm_button = tk.Radiobutton(tester_frame, text="Yes", variable=worm_profile_var, value=True)
yes_worm_button.grid(row=4, column=1, sticky='w')

no_worm_button = tk.Radiobutton(tester_frame, text="No", variable=worm_profile_var, value=False)
no_worm_button.grid(row=4, column=2, sticky='w')

# Radio buttons for "follow_each_other" Yes/No option
follow_each_other_var = tk.BooleanVar(value=True)  # Default to Yes (True)
tk.Label(tester_frame, text='Follow each other?').grid(row=5, column=0, padx=5, pady=5, sticky='e')

yes_follow_button = tk.Radiobutton(tester_frame, text="Yes", variable=follow_each_other_var, value=True)
yes_follow_button.grid(row=5, column=1, sticky='w')

no_follow_button = tk.Radiobutton(tester_frame, text="No", variable=follow_each_other_var, value=False)
no_follow_button.grid(row=5, column=2, sticky='w')

# Create buttons for starting and stopping worming
btn_start_worming = tk.Button(tester_frame, text='Start worming', command=start_worming_the_accs)
btn_start_worming.grid(row=6, column=1, padx=10, pady=10, sticky='nsew')

btn_stop_worming = tk.Button(tester_frame, text='Stop worming', command=stop_worming)
btn_stop_worming.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')



def add_sleep_to_test_accounts(widget,main):
  bot_name=get_user_name_and_pass()
  if bot_name:
    # Gather data from entry fields
    min_minute = widget.get()

    # Validate if all fields are filled
    if min_minute == '' :
        messagebox.showerror('Error', 'Please fill in sleep time')
        return

    # Format the data
    Numbers_data = f"{min_minute},\n"

    # Append data to the file
    if main == 'main':
     with open(f'needs/Numbers_sleep_in_test_{bot_name}_.txt', 'w',encoding='utf-8') as file:
        file.write(Numbers_data)
    elif main == 'scraper' :
        with open(f'needs/Numbers_sleep_in_test_scraper_{bot_name}_.txt', 'w',encoding='utf-8') as file:
         file.write(Numbers_data)
    
    # Clear and set placeholder text
    widget.delete(0, tk.END)
    widget.insert(0, min_minute)

    messagebox.showinfo('Success', 'Numbers added successfully')
    return True
  else:
      messagebox.showerror("Error", "No user selected")
      return False


def load_data_of_sleep_test(widget,main):
    bot_name=get_user_name_and_pass()
    try:
        if main =='main':
         with open(f'needs/Numbers_sleep_in_test_{bot_name}_.txt', 'r', encoding='utf-8') as file:
            data = file.readline().strip().split(',')
            if len(data) >= 1:
                # Clear existing content
                widget.delete(0, tk.END)
                # inserting data
                widget.insert(0, data[0])
        elif main == 'scraper':
         with open(f'needs/Numbers_sleep_in_test_scraper_{bot_name}_.txt', 'r', encoding='utf-8') as file:
            data = file.readline().strip().split(',')
            if len(data) >= 1:
                # Clear existing content
                widget.delete(0, tk.END)
                # inserting data
                widget.insert(0, data[0])
              
    except FileNotFoundError:
        # Clear existing content
        widget.delete(0, tk.END)
        messagebox.showwarning(
            'Warning', 'sleep between login to test accounts.')


def validate_numeric_input2(action, value_if_allowed):
    # action: 1 = insert, 0 = delete
    if action == '1':
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return True

# Create labels and entry fields for proxy information
validate_numeric2=tester_frame.register(validate_numeric_input2)
tk.Label(tester_frame, text='Sleep after login for (seconds)').grid(
    row=0, column=0, padx=5, pady=5, sticky='e')
tk.Label(tester_frame, text='To get login code').grid(
    row=0, column=1, padx=1, pady=1, sticky='e')
entry_min_minute2 = tk.Entry(tester_frame, width=5, validate='key',
                            validatecommand=(validate_numeric2, '%d', '%P'))
entry_min_minute2.grid(row=0, column=1, padx=5, pady=5, sticky='w')


# Initial data load
refresh_data_a1()


# Widgets for frame3 (proxy management)
tk.Label(frame3, text='Proxy Data', font=("Helvetica", 16)).grid(
    row=0, columnspan=2, padx=10, pady=10)

tk.Label(frame3, text='Proxy Host').grid(row=1, column=0, padx=10, pady=5)
entry_host = tk.Entry(frame3)
entry_host.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame3, text='Proxy Port').grid(row=2, column=0, padx=10, pady=5)
entry_port = tk.Entry(frame3)
entry_port.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame3, text='User Name').grid(row=3, column=0, padx=10, pady=5)
entry_user = tk.Entry(frame3)
entry_user.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame3, text='Password').grid(row=4, column=0, padx=10, pady=5)
entry_password = tk.Entry(frame3)
entry_password.grid(row=4, column=1, padx=10, pady=5)

btn_add = tk.Button(frame3, text='Add Proxy', command=add_proxy, width=20)
btn_add.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')


# # Create widgets for the DM Sending tab
# dm_label = tk.Label(dm_frame, text="DM Sending Functionality Placeholder")
# dm_label.pack(pady=5)
# dm_button = tk.Button(dm_frame, text="Send DM", command=dummy_dm_sending_function)
# dm_button.pack(pady=5)


# ////////////////// second page


# Common functions for handling CSV data
def save_data_list_csv(data_list, data_type):
    bot_name=get_user_name_and_pass()
    filename = f"needs/message/{data_type}_{bot_name}_.csv"
    data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row[0])
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data_list:
            if item not in data:
                writer.writerow([item])


def data_exists(data_type):
    bot_name=get_user_name_and_pass()
    viv=f"{data_type}_{bot_name}_"
    folder_path = "needs/message"
    for file_name in os.listdir(folder_path):
        if file_name.startswith(viv):
            return True
    return False


def get_all_data(data_type):
    data_list = []
    if data_exists(data_type):
        folder_path = "needs/message"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            viv=f"{data_type}_{bot_name}_"
            if file_name.startswith(viv):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        data_list.append(row[0])
    return data_list


def delete_data(data_type):
    if data_exists(data_type):
        folder_path = "needs/message"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            viv=f"{data_type}_{bot_name}_"   
            if file_name.startswith(viv):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                deleted = True
        return deleted
    return False


def delete_row_from_csv(data_type, row_data):
    if data_exists(data_type):
        folder_path = "needs/message"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            viv=f"{data_type}_{bot_name}_"
            if file_name.startswith(viv):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    if row[0] == row_data:
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False

# GUI Functions

def save_data_gui(data_type, text_widget):
    data_input = text_widget.get("1.0", tk.END).strip()
    if data_input:
        bot_name = get_user_name_and_pass()
        if bot_name:
            save_data_list_csv([data_input], data_type)
            messagebox.showinfo("Success", f"{data_type.capitalize()} saved to CSV file")
            text_widget.delete("1.0", tk.END)  # Clear the text widget after saving
            refresh_data_list(data_type)  # Refresh the list after adding new data
        else:
            messagebox.showerror("Error", "No user selected")
    else:
        messagebox.showerror("Error", f"{data_type.capitalize()} not provided")


def get_all_data_gui(data_type, frame):
    clear_frame(frame)
    all_data = get_all_data(data_type)
    if all_data:
        for data in all_data:
            row_frame = tk.Frame(frame)
            row_frame.pack(fill='x', padx=5, pady=2)

            data_label = tk.Label(row_frame, text=data, anchor='w', justify='left', wraplength=200)
            data_label.pack(side='left', fill='x', expand=True)

            delete_button_ = tk.Button(row_frame, text="Delete", command=lambda data=data: delete_data_row(data_type, data))
            delete_button_.pack(side='right')
    else:
        tk.Label(frame, text=f"No {data_type}s found").pack()


def add_data_gui(data_type, input_frame):
    add_data_frame = tk.Frame(input_frame)
    add_data_frame.pack(fill='x', pady=5)
    tk.Label(add_data_frame, text=f"Add new {data_type}:").pack(side='top', padx=5)
    new_data_text = tk.Text(add_data_frame, height=5, width=40)
    new_data_text.pack(side='top', fill='x', expand=True, padx=5, pady=5)
    add_button = tk.Button(add_data_frame, text="Add", command=lambda: save_data_gui(data_type, new_data_text))
    add_button.pack(side='top', padx=5, pady=5)


def add_new_data(data_type, data):
    if data:
        save_data_list_csv([data], data_type)
        messagebox.showinfo("Success", f"{data_type.capitalize()} '{data}' added.")
        refresh_data_list(data_type)  # Refresh the list after adding new data
    else:
        messagebox.showerror("Error", f"{data_type.capitalize()} not provided")


def delete_data_row(data_type, data):
    if delete_row_from_csv(data_type, data):
        messagebox.showinfo("Success", f"{data_type.capitalize()} '{data}' deleted.")
        refresh_data_list(data_type)  # Refresh the list after deleting data
    else:
        messagebox.showerror("Error", f"{data_type.capitalize()} '{data}' not found.")


def refresh_data_list(data_type):
    if data_type == 'intro':
        get_all_data_gui('intro', intros_content_frame)
    elif data_type == 'body':
        get_all_data_gui('body', bodies_content_frame)
    elif data_type == 'outro':
        get_all_data_gui('outro', outros_content_frame)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Copy to clipboard function
def copy_to_clipboard(text):
    GUI.clipboard_clear()
    GUI.clipboard_append(text)
    GUI.update()  # now it stays on the clipboard after the window is closed
    messagebox.showinfo("Copied", "Text copied to clipboard")


# Frame for the message about <Account-name>
info_frame = tk.Frame(dm_frame)
info_frame.pack(pady=5)

info_label = tk.Label(info_frame, text="To display the name use this ")
info_label.pack(side='left')

account_name_button = tk.Button(info_frame, text="<Account-name>", command=lambda: copy_to_clipboard("<Account-name>"))
account_name_button.pack(side='left')

# Main frame for aligning sections horizontally
main_frame = tk.Frame(dm_frame)
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Helper function to create a scrollable frame with an input section below it
def create_scrollable_frame_with_input(parent_frame, label_text, data_type):
    outer_frame = tk.Frame(parent_frame, bd=2, relief='sunken')
    outer_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)
    
    # Scrollable content frame
    canvas = tk.Canvas(outer_frame)
    canvas.pack(side='top', fill='both', expand=True)

    scrollbar_data = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollbar_data.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar_data.set)

    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Add label at the top of the scrollable content
    tk.Label(outer_frame, text=label_text).pack()

    # Input frame below the scrollable content
    input_frame = tk.Frame(outer_frame)
    input_frame.pack(side='bottom', fill='x', pady=5)
    add_data_gui(data_type, input_frame)

    return content_frame

# Create intros, bodies, and outros frames with scrollbars and input sections
intros_content_frame = create_scrollable_frame_with_input(main_frame, "Intros", 'intro')
bodies_content_frame = create_scrollable_frame_with_input(main_frame, "Bodies", 'body')
outros_content_frame = create_scrollable_frame_with_input(main_frame, "Outros", 'outro')

# Refresh data lists
refresh_data_list('intro')
refresh_data_list('body')
refresh_data_list('outro')


#  for numeric and start function


def validate_numeric_input(action, value_if_allowed):
    # action: 1 = insert, 0 = delete
    if action == '1':
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return True


def add_numeric_data():
  bot_name=get_user_name_and_pass()
  if bot_name:
    # Gather data from entry fields
    min_minute = limit_of_one_account.get()
    stop_on_reach = entry_stop_on_reach.get()

    # Validate if all fields are filled
    if min_minute == ''  or stop_on_reach == '':
        messagebox.showerror('Error', 'Please fill in all fields')
        return

    # Format the data
    Numbers_data = f"{min_minute},{stop_on_reach}\n"

    # Append data to the file

    with open(f'needs/Numbers_{bot_name}_.txt', 'w',encoding='utf-8') as file:
        file.write(Numbers_data)

    # Clear and set placeholder text
    limit_of_one_account.delete(0, tk.END)
    limit_of_one_account.insert(0, min_minute)

    entry_stop_on_reach.delete(0, tk.END)
    entry_stop_on_reach.insert(0, stop_on_reach)

    messagebox.showinfo('Success', 'Numbers added successfully')
  else:
      messagebox.showerror("Error", "No user selected")

def data_messages_check(data_type):
        bot_name=get_user_name_and_pass()
        folder_path = "needs/message"
        a8a=False
        for file_name in os.listdir(folder_path):
         viv=f"{data_type}_{bot_name}_"
         if file_name.startswith(viv):
           a8a=True
        return  a8a               
        

def start_the_bot():
    bot_name=get_user_name_and_pass()
    with open(f'got_messages_{bot_name}_.csv','w',encoding='utf-8')as f:
                f.write('start')
    csv_file_path=f"needs/bot_{bot_name}_.csv"
    if bot_name:
        add_numeric_data()
        save_link()
        if not users_data_func():
             messagebox.showerror("Error", "You havent add people to text them")
             return 
        folder_path = "needs"
        a7a=False
        for file_name in os.listdir(folder_path):
         if file_name.startswith(f"Numbers_{bot_name}_"):
           a7a=True
        if not a7a :
             messagebox.showerror("Error", "You havent added delays between messages.")
             return   
        if not  data_messages_check('intro'):
             messagebox.showerror("Error", "You havent add intro to the messages")
             return 
        if not  data_messages_check('body'):
             messagebox.showerror("Error", "You havent add body to the messages")
             return 
        if not  data_messages_check('outro'):
             messagebox.showerror("Error", "You havent add outro to the messages")
             return 
        messagebox.showinfo("Success", "Press Ok to Start the bot ")
        thread2 = threading.Thread(target=worker_1, args=(bot_name,csv_file_path))
        thread2.start()
    else:
     messagebox.showerror("Error", "No user selected")


# Frame for numeric input validation and entry fields
numeric_frame = tk.Frame(dm_frame, bd=2, relief='sunken')
numeric_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Validation functions for numeric input
validate_numeric = dm_frame.register(validate_numeric_input)

# Create labels and entry fields for proxy information
tk.Label(numeric_frame, text='send (msg)').grid(
    row=0, column=0, padx=5, pady=5, sticky='e')
limit_of_one_account = tk.Entry(numeric_frame, width=5, validate='key',
                            validatecommand=(validate_numeric, '%d', '%P'))
limit_of_one_account.grid(row=0, column=1, padx=5, pady=5, sticky='w')

tk.Label(numeric_frame, text='per acount in the bot [max is 50 per day]').grid(
    row=0, column=1, padx=5, pady=5, sticky='e')

tk.Label(numeric_frame, text='Stop the Bot after (msg)').grid(
    row=2, column=0, padx=5, pady=5, sticky='e')
entry_stop_on_reach = tk.Entry(
    numeric_frame, width=5, validate='key', validatecommand=(validate_numeric, '%d', '%P'))
entry_stop_on_reach.grid(row=2, column=1, padx=5,
                         pady=5, sticky='w', columnspan=3)

# New widgets for link input
def save_link():
    bot_name=get_user_name_and_pass()
    if bot_name:
     link = entry_link.get()
     if link:
      with open(f"needs/post_{bot_name}_.txt", 'w', encoding="utf-8") as file:
        file.write(link)
      entry_link.delete(0, tk.END)
      entry_link.insert(0, link)
     else:
        messagebox.showerror("Error", "plz add the link first")

    else:
       messagebox.showerror("Error", "No user selected")
    

# Function to load the link from the file
def load_link():
    bot_name=get_user_name_and_pass()
    try:
        with open(f"needs/post_{bot_name}_.txt", 'r', encoding="utf-8") as file:
            link = file.read().strip()
            entry_link.insert(0, link)
    except FileNotFoundError:
        pass

tk.Label(numeric_frame, text='Enter Instagram post Link').grid(row=3, column=0, padx=5, pady=5, sticky='e')
entry_link = tk.Entry(numeric_frame, width=70)
entry_link.grid(row=3, column=1, padx=5, pady=5, sticky='w', columnspan=3)


# Create button for adding data
btn_add = tk.Button(numeric_frame, text='Start The Bot',
                    command=start_the_bot, width=20)
btn_add.grid(row=5, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')


def load_data_numeric():
    bot_name=get_user_name_and_pass()
    try:
        with open(f'needs/Numbers_{bot_name}_.txt', 'r', encoding='utf-8') as file:
            data = file.readline().strip().split(',')
            if len(data) >= 2:
                # Clear existing content
                limit_of_one_account.delete(0, tk.END)
                entry_stop_on_reach.delete(0, tk.END)

                # inserting data
                limit_of_one_account.insert(0, data[0])
                entry_stop_on_reach.insert(0, data[1])
    except FileNotFoundError:
        # Clear existing content
        limit_of_one_account.delete(0, tk.END)
        entry_stop_on_reach.delete(0, tk.END)
        messagebox.showwarning(
            'Warning', 'Data file not found. Default values will be used.')


def load_data_proxy():
    bot_name=get_user_name_and_pass()
    try:
        with open(f'needs/proxy_{bot_name}_.txt', 'r', encoding='utf-8') as file:
            data = file.readline().strip().split(',')
            if len(data) == 4:
                # Clear existing content
                entry_host.delete(0, tk.END)
                entry_port.delete(0, tk.END)
                entry_user.delete(0, tk.END)
                entry_password.delete(0, tk.END)
                
                # Insert new data
                entry_host.insert(0, data[0])
                entry_port.insert(0, data[1])
                entry_user.insert(0, data[2])
                entry_password.insert(0, data[3])
    except FileNotFoundError:
        # Clear existing content
        entry_host.delete(0, tk.END)
        entry_port.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        messagebox.showwarning('Warning', 'Data file not found. plz add proxy')


#  The Scraper Part //////////////////////////////////////////////////////////////////////////////////////////////////

def download_file():
    try:
        # Open a file dialog to choose where to save the file
        username,password=get_account_for_scrape()
        if username:
         bot_name=get_user_name_and_pass()
         needed_file=[]
         files=os.listdir('scrape')
         for file in files :
             if file.startswith(f'filtered_data_{bot_name}_'):
                 needed_file.append(file)
         if needed_file:
          the_file=needed_file[0]

          save_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                 initialfile=f"Scraped-data.csv")
          if save_path:
            # Copy the file to the chosen location
            shutil.copyfile(f'scrape/{the_file}', save_path)
            messagebox.showinfo("Success", f"File downloaded successfully as '{save_path}'")
         else:
            messagebox.showerror("Error", "plz start scrap first")
        else:
            messagebox.showerror("Error", "No scrape account")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def users_data_func_for_scraper():
    folder_path = "scrape"
    for file_name in os.listdir(folder_path):
        bot_name=get_user_name_and_pass()
        if file_name.startswith(f"filtered_data_{bot_name}_"):
            return True
    return False

def get_all_uses_data_for_scraper():
    users_data = []
    if users_data_func_for_scraper():
        folder_path = "scrape"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"filtered_data_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    try:
                        next(csv_reader)  # Skip the header row
                    except StopIteration:
                        # Handle the case where the CSV file is empty or only has a header
                        continue
                    for row in csv_reader:
                        users_data.append(row[:2])  # Get only the first 2 columns

    return users_data

def delete_all_users_data_for_scraper():
    if users_data_func_for_scraper():
        folder_path = "scrape"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"filtered_data_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                deleted = True
            folder_path1='data'
            for file_sub in os.listdir(folder_path1):
             if file_sub.startswith(f"data_{bot_name}_") or file_sub.startswith(f"full_data_{bot_name}_"):
                file_path1 = os.path.join(folder_path1, file_sub)
                os.remove(file_path1)
        return deleted
    return False

def delete_user_from_csv_for_scraper(intro):
    if users_data_func_for_scraper():
        folder_path = "scrape"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"filtered_data_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    if row[:2] == intro:
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False
# Global references to Treeview and related widgets, initialized to None
tree1 = None
scrollbar1 = None
delete_button1 = None
tree_frame1=None
num_accounts_label7=None
def show_current_data_for_scraper():
    global tree1, scrollbar1, delete_button1 ,tree_frame1,num_accounts_label7 # Use global references to these widgets
    all_users = get_all_uses_data_for_scraper()
    if all_users:
        # Clear previous instances, if any
        if tree1:
            tree1.destroy()
        if scrollbar1:
            scrollbar1.destroy()
        if delete_button1:
            delete_button1.destroy()
        if tree_frame1 :
            tree_frame1.destroy()
        if num_accounts_label7 :
            num_accounts_label7.destroy()
        # Create a frame to hold the Treeview and scrollbar1
        tree_frame1 = tk.Frame(scrape_frame_1)
        tree_frame1.pack(fill=tk.BOTH, expand=True)


        # Create a Treeview
        tree1 = ttk.Treeview(tree_frame1, columns=('Username', 'Full name'), show='headings')
        tree1.heading('Username', text='Username')
        tree1.heading('Full name', text='Full name')
        tree1.column('Username', width=150)
        tree1.column('Full name', width=320)
        
        # Add data to the Treeview
        for intro in all_users:
            tree1.insert('', tk.END, values=intro)

        # Add a Scrollbar
        scrollbar1 = ttk.Scrollbar(tree_frame1, orient=tk.VERTICAL, command=tree1.yview)
        tree1.configure(yscroll=scrollbar1.set)
        
        # Pack the Treeview and Scrollbar inside the tree_frame
        tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        
         # Add a label to show the number of accounts found
        if num_accounts_label3 is None:
           num_accounts_label7 = tk.Label(scrape_frame_1, text=f"Number of users found: {len(all_users)}")
           num_accounts_label7.pack( pady=2)
        else:
              num_accounts_label7.destroy()
              num_accounts_label7 = tk.Label(scrape_frame_1, text=f"Number of users found: {len(all_users)}")
              num_accounts_label7.pack( pady=2)
        # Add delete button below the tree_frame
        def delete_selected():
            selected_items = tree1.selection()
            for selected_item in selected_items:
                item_values = tree1.item(selected_item)['values']
                if delete_user_from_csv_for_scraper(item_values):
                    tree1.delete(selected_item)
                    num_accounts_label7.config(text=f"Number of users found: {len(tree1.get_children())}")


        delete_button1 = tk.Button(scrape_frame_1, text="Delete Selected", command=delete_selected, width=20)
        delete_button1.pack(pady=5)
    else:
        if tree1:
            tree1.destroy()
        if scrollbar1:
            scrollbar1.destroy()
        if delete_button1:
            delete_button1.destroy()
        if tree_frame1 :
            tree_frame1.destroy()
        if num_accounts_label7 :
            num_accounts_label7.destroy()
        messagebox.showerror("Error", "No scraped data")

def delete_intro_and_refresh(window, intro):
    if delete_user_from_csv_for_scraper(intro):
        messagebox.showinfo("Success", f"Intro '{', '.join(intro)}' deleted")
        window.destroy()
        show_current_data_for_scraper()
    else:
        messagebox.showerror("Error", f"Intro '{', '.join(intro)}' not found")

def delete_all_usesrs__for_scraper():
    if delete_all_users_data_for_scraper():
        messagebox.showinfo("Success", "All users deleted")
        refresh_username()
    else:
        messagebox.showerror("Error", "No users to delete")

# def start_scrape():
#     accounts = read_from_test_csv_for_scrape()
#     if accounts:
#         username=accounts[0]['email']
#         password=accounts[0]['password']
#         messagebox.showinfo("Success", "Press Ok to Start the bot ")
#         thread3 = threading.Thread(target=get_cutomers, args=(username,password))
#         thread3.start()
#     else:
#      messagebox.showerror("Error", "No scrape accound added")
    
#  email part of the scraper

# Functions from the second script

def users_data_func___a_a_for_scraper():
    folder_path = "needs"
    for file_name in os.listdir(folder_path):
        bot_name=get_user_name_and_pass()
        if file_name.startswith(f"scrape_emails_all_{bot_name}_"):
            return True
    return False

def get_all_users_data___aa1_scraper():
    users_data = []
    if users_data_func___a_a_for_scraper():
        folder_path = "needs"
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"scrape_emails_all_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        users_data.append([row[0], row[1]])  # Get the first two columns (username and password)
                    
    return users_data

def delete_user_from_csv____a_a1_scraper(intro):
    if users_data_func___a_a_for_scraper():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"scrape_emails_all_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    rows = list(csv_reader)
                for row in rows[:]:
                    if row[0] == intro[0]:  # Check the first column (username)
                        rows.remove(row)
                        deleted = True
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        return deleted
    return False


def delete_all_users_data___a_a_scraper():
    if users_data_func___a_a_for_scraper():
        folder_path = "needs"
        deleted = False
        for file_name in os.listdir(folder_path):
            bot_name=get_user_name_and_pass()
            if file_name.startswith(f"scrape_emails_all_{bot_name}_"):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                deleted = True
        return deleted
    return False

def refresh_data_a1_scraper():
    global combo_scraper

    users = get_all_users_data___aa1_scraper()
    
    combo_scraper['values'] = [f"{user[0]} ({user[1]})" for user in users]
    # combo_scraper['values'] = [f"  {user[0]}" for user in users]
    
    if users:
        combo_scraper.current(0)  # Set the first item as selected
    else:
        combo_scraper.set('')
   
    

def delete_selected_a1_scraper():
    selected_item = combo_scraper.get()
    if selected_item:
        username = selected_item.split(" ")[0]
        if delete_user_from_csv____a_a1_scraper([username]):
            refresh_data_a1_scraper()
            use_selected_1_scraper()
            refresh_username()

def use_selected_1_scraper():
    selected_item = combo_scraper.get()
    print(selected_item)
    if selected_item:
        username, password = selected_item.split(" ")[0], selected_item.split(" ")[1][1:-1]
        bot_name=get_user_name_and_pass()
        with open(f"needs/scrape_email{bot_name}_.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # writer.writerow(["username", "password"])  # Write the header
            writer.writerow([username, password])
        messagebox.showinfo("Success", "Selected data saved to data.csv")
    refresh_username()



def save_test_account_data_aa_scraper(email, password):
    bot_name=get_user_name_and_pass()
    with open(f'needs/scrape_emails_all_{bot_name}_.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])
    refresh_data_a1_scraper()  # Update the accounts display


def add_account_scraper():
    email = email_entry_scraper.get()
    password = password_entry_scraper.get()
    bot_name=get_user_name_and_pass()
    if bot_name:
     if email and password:
      if add_sleep_to_test_accounts(entry_min_minute2_scrape,'scraper'):
        messagebox.showinfo("Success", "Press OK to login and wait the login will take time dont terminate the pop window of instagram")
        
        if login_to_insta(email, password,bot_name):
            save_test_account_data_aa_scraper(email, password)
            refresh_username()
            password_entry_scraper.delete(0, tk.END)
            email_entry_scraper.delete(0, tk.END)
        else:
             messagebox.showwarning("Error", "Login failed, check your username or password")
     else:
        messagebox.showwarning("Input Error", "Please enter both email and password.")
    else:
       messagebox.showerror("Error", "No bot selected")



def get_account_for_scrape():
    selected_item = combo_scraper.get()
    password,username='',''
    if selected_item:
        username, password = selected_item.split(" ")[0], selected_item.split(" ")[1][1:-1]
    return username,password


# part of the filteres
# import pandas as pd
# from langdetect import detect, LangDetectException
import json

# Path to the JSON file for saving filter settings

def save_settings_1(settings):
    email_scraper,password_scraper=get_account_for_scrape()
    if email_scraper:
     bot_name=get_user_name_and_pass()
     with open(f'scrape/filter_settings_{bot_name}_.json', 'w',encoding='utf-8') as f:
        json.dump(settings, f)
    else:
       messagebox.showerror("Error", "No scrape email added")

def load_settings_1():
    bot_name=get_user_name_and_pass()
    file_name = f"filter_settings_{bot_name}_.json"
    file_path = os.path.join("scrape", file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding='utf-8') as f:
            return json.load(f)
    return {}

def apply_filters():
  email_scraper,password_scraper=get_account_for_scrape()
  if email_scraper:
    apply_phone_codes = phone_codes_var.get()
    phone_codes = phone_codes_entry.get()
    phone_codes = [int(code.strip()) for code in phone_codes.split(',')] if phone_codes else []

    apply_min_followers = min_followers_var.get()
    min_followers = int(min_followers_entry.get()) if min_followers_entry.get() else 0

    apply_bio_lang = bio_lang_var.get()

    apply_is_private = is_private_var.get()
    is_private = is_private_value.get()

    apply_is_business = is_business_var.get()
    is_business = is_business_value.get()

    apply_is_verified = is_verified_var.get()
    is_verified = is_verified_value.get()

    apply_avatar_link = avatar_link_var.get()

    apply_full_name = full_name_var.get()
    
    apply_min_posts = min_posts_var.get()
    min_posts = int(min_posts_entry.get()) if min_posts_entry.get() else 0

    apply_bio_words = bio_words_var.get()
    bio_words = bio_words_entry.get()
    include_exclude = include_exclude_var.get()

    # filter_data(
    #     apply_phone_codes, phone_codes, apply_min_followers, min_followers, apply_bio_lang, 
    #     apply_is_private, is_private, apply_is_business, is_business, apply_is_verified, 
    #     is_verified, apply_avatar_link, apply_full_name, apply_min_posts, min_posts
    # )

    # Save settings
    settings = {
        "apply_phone_codes": apply_phone_codes,
        "phone_codes": phone_codes_entry.get(),
        "apply_min_followers": apply_min_followers,
        "min_followers": min_followers_entry.get(),
        "apply_bio_lang": apply_bio_lang,
        "apply_is_private": apply_is_private,
        "is_private": is_private,
        "apply_is_business": apply_is_business,
        "is_business": is_business,
        "apply_is_verified": apply_is_verified,
        "is_verified": is_verified,
        "apply_avatar_link": apply_avatar_link,
        "apply_full_name": apply_full_name,
        "apply_min_posts": apply_min_posts,
        "min_posts": min_posts_entry.get(),
        "apply_bio_words": apply_bio_words,
        "bio_words": bio_words_entry.get(),
        "include_exclude": include_exclude
    }
    save_settings_1(settings)

def load_saved_settings():
    settings = load_settings_1()
    phone_codes_var.set(settings.get("apply_phone_codes", False))
    phone_codes_entry.insert(0, settings.get("phone_codes", ""))

    min_followers_var.set(settings.get("apply_min_followers", False))
    min_followers_entry.delete(0, 'end')
    min_followers_entry.insert(0, settings.get("min_followers", "1000"))

    bio_lang_var.set(settings.get("apply_bio_lang", False))

    is_private_var.set(settings.get("apply_is_private", False))
    is_private_value.set(settings.get("is_private", "NO"))

    is_business_var.set(settings.get("apply_is_business", False))
    is_business_value.set(settings.get("is_business", "NO"))

    is_verified_var.set(settings.get("apply_is_verified", False))
    is_verified_value.set(settings.get("is_verified", "No"))

    avatar_link_var.set(settings.get("apply_avatar_link", False))

    full_name_var.set(settings.get("apply_full_name", False))
    
    min_posts_var.set(settings.get("apply_min_posts", False))
    min_posts_entry.delete(0, 'end')
    min_posts_entry.insert(0, settings.get("min_posts", "1"))

    bio_words_var.set(settings.get("apply_bio_words", False))
    bio_words_entry.insert(0, settings.get("bio_words", ""))
    include_exclude_var.set(settings.get("include_exclude", "include"))

# specify the inputs part for scraper
def save_settings_for_scraper_type():
  email_scraper,password_scraper=get_account_for_scrape()
  if email_scraper:
    type_of_agent = agent_type_var.get()
    My_hashtag = hashtag_entry.get()
    tracker = tracker_var.get()
    extract_profiles = extract_profiles_var.get()
    settings = {
        "type_of_agent": type_of_agent,
        "My_hashtag": My_hashtag,
        "tracker": tracker,
        "extract_profiles": extract_profiles
    }
    bot_name=get_user_name_and_pass()
    with open(f"scrape/settings_{bot_name}_.json", "w",encoding='utf-8') as file:
        json.dump(settings, file)
    if My_hashtag:
      Thread(target=main_scraper, args=(type_of_agent, My_hashtag,email_scraper,password_scraper,tracker,bot_name,extract_profiles)).start()
    else:
         messagebox.showerror("Error", "add data plz")
  else:
       messagebox.showerror("Error", "No scrape email added")

def load_settings_for_scraper_type():
    bot_name=get_user_name_and_pass()
    file_name = f"settings_{bot_name}_.json"
    file_path = os.path.join("scrape", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r",encoding='utf-8') as file:
            settings = json.load(file)
            agent_type_var.set(settings.get("type_of_agent", "followers"))
            hashtag_entry.delete(0, tk.END)
            hashtag_entry.insert(0, settings.get("My_hashtag", ""))
            tracker_var.set(settings.get("tracker", "middile"))
            extract_profiles_var.set(settings.get("extract_profiles", False))


# for the proxy 

def add_proxy_scraper():
    # Gather data from entry fields
    proxy_host_scraper = entry_host_scraper.get()
    proxy_port_scraper = entry_port_scraper.get()
    user_name_scraper = entry_user_scraper.get()
    password_scraper = entry_password_scraper.get()

    # Validate if all fields are filled
    if proxy_host_scraper == '' or proxy_port_scraper == '' or user_name_scraper == '' or password_scraper == '':
        messagebox.showerror('Error', 'Please fill in all fields')
        return

    # Format the data
    proxy_data = f"{proxy_host_scraper},{proxy_port_scraper},{user_name_scraper},{password_scraper}\n"
    
    username_,password_=get_account_for_scrape()
    if username_:
     bot_name=get_user_name_and_pass()
     # Append data to the file
     with open(f'needs/proxy_{bot_name}_scrape_.txt', 'w', encoding='utf-8') as file:
        file.write(proxy_data)

     # Set placeholder text
     entry_host_scraper.delete(0, tk.END)
     entry_host_scraper.insert(0, proxy_host_scraper)

     entry_port_scraper.delete(0, tk.END)
     entry_port_scraper.insert(0, proxy_port_scraper)

     entry_user_scraper.delete(0, tk.END)
     entry_user_scraper.insert(0, user_name_scraper)

     entry_password_scraper.delete(0, tk.END)
     entry_password_scraper.insert(0, password_scraper)

     messagebox.showinfo('Success', 'Proxy data added successfully')
    else:
     messagebox.showerror("Error", "No user selected")


def load_data_proxy_scraper():
    bot_name=get_user_name_and_pass()
    try:
        with open(f'needs/proxy_{bot_name}_scrape_.txt', 'r', encoding='utf-8') as file:
            data = file.readline().strip().split(',')
            if len(data) == 4:
                # Clear existing content
                entry_host_scraper.delete(0, tk.END)
                entry_port_scraper.delete(0, tk.END)
                entry_user_scraper.delete(0, tk.END)
                entry_password_scraper.delete(0, tk.END)
                
                # Insert new data
                entry_host_scraper.insert(0, data[0])
                entry_port_scraper.insert(0, data[1])
                entry_user_scraper.insert(0, data[2])
                entry_password_scraper.insert(0, data[3])
    except FileNotFoundError:
        # Clear existing content
        entry_host_scraper.delete(0, tk.END)
        entry_port_scraper.delete(0, tk.END)
        entry_user_scraper.delete(0, tk.END)
        entry_password_scraper.delete(0, tk.END)
        messagebox.showwarning('Warning', 'Data file not found. plz add proxy fpr scraper')




# the four frames part



def create_frame(parent, row, column, sticky, borderwidth=2, relief='sunken'):
    frame = tk.Frame(parent, bd=borderwidth, relief=relief)
    frame.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)
    return frame
# Configure the grid to have equal weight for resizing
Scraper_frame.grid_rowconfigure(0, weight=1)
Scraper_frame.grid_rowconfigure(2, weight=1)
Scraper_frame.grid_columnconfigure(0, weight=1)
Scraper_frame.grid_columnconfigure(2, weight=1)

# Create frames in each corner with borders
scrape_frame_1 = create_frame(Scraper_frame, 0, 0, 'nsew')
scrape_frame_2 = create_frame(Scraper_frame, 0, 2, 'nsew')
scrape_frame_3 = create_frame(Scraper_frame, 2, 0, 'nsew')
scrape_frame_4 = create_frame(Scraper_frame, 2, 2, 'nsew')

# scrape_frame_1 = tk.Frame(Scraper_frame, padx=10, pady=10, bd=1,relief='sunken')
# scrape_frame_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# scrape_frame_2 = tk.Frame(Scraper_frame, padx=10, pady=10, bd=1,relief='sunken')
# scrape_frame_2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)



# Create the top frame
top_frame = tk.Frame(scrape_frame_3, height=100)
top_frame.pack(fill='both', expand=True)

# Create the bottom frame
bottom_frame = tk.Frame(scrape_frame_3, height=100)
bottom_frame.pack(fill='both', expand=True)

# the proxy frame 

# Widgets for frame3 (proxy management)
tk.Label(top_frame, text='Proxy Data', font=("Helvetica", 16)).grid(
    row=0, columnspan=2, padx=10, pady=10)

tk.Label(top_frame, text='Proxy Host').grid(row=1, column=0, padx=10, pady=5)
entry_host_scraper = tk.Entry(top_frame)
entry_host_scraper.grid(row=1, column=1, padx=10, pady=5)

tk.Label(top_frame, text='Proxy Port').grid(row=2, column=0, padx=10, pady=5)
entry_port_scraper = tk.Entry(top_frame)
entry_port_scraper.grid(row=2, column=1, padx=10, pady=5)

tk.Label(top_frame, text='User Name').grid(row=3, column=0, padx=10, pady=5)
entry_user_scraper = tk.Entry(top_frame)
entry_user_scraper.grid(row=3, column=1, padx=10, pady=5)

tk.Label(top_frame, text='Password').grid(row=4, column=0, padx=10, pady=5)
entry_password_scraper = tk.Entry(top_frame)
entry_password_scraper.grid(row=4, column=1, padx=10, pady=5)

btn_add_scraper = tk.Button(top_frame, text='Add Proxy', command=add_proxy_scraper, width=20)
btn_add_scraper.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')



# Create and set variables
agent_type_var = tk.StringVar(value="followers")
tracker_var = tk.StringVar(value="middile")
extract_profiles_var = tk.BooleanVar(value=False)

# Create widgets
agent_type_label = tk.Label(bottom_frame, text="Type of Agent:")
agent_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
agent_type_menu = ttk.Combobox(bottom_frame, textvariable=agent_type_var, values=["followers", "following", "hashtag","location"])
agent_type_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

hashtag_label = tk.Label(bottom_frame, text="user or hashtag or location link:")
hashtag_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
hashtag_entry = tk.Entry(bottom_frame)
hashtag_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

tracker_label = tk.Label(bottom_frame, text="Tracker:")
tracker_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
tracker_menu = ttk.Combobox(bottom_frame, textvariable=tracker_var, values=["no-time", "max-time", "middile","just-before-middile"])
tracker_menu.grid(row=2, column=1, padx=10, pady=10, sticky="ew")


extract_profiles_check = tk.Checkbutton(bottom_frame, text="Extract Profiles", variable=extract_profiles_var)
extract_profiles_check.grid(row=3, column=0, padx=10, pady=10, sticky="w")


start_button = tk.Button(bottom_frame, text="Start Scraping", command=save_settings_for_scraper_type)
start_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


# here the ui of the filters  

def only_numbers(char):
    return char.isdigit()

# Validation command for numeric input
vcmd = (GUI.register(only_numbers), '%S')

# Function to allow only numeric input and commas
def only_numbers_and_commas(char):
    return char.isdigit() or char == ','

vcmd_numbers_commas = (GUI.register(only_numbers_and_commas), '%S')

# Checkbox and input for minimum followers count
min_followers_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Minimum Followers Count", variable=min_followers_var).grid(row=0, column=0, padx=10, pady=10, sticky='w')
min_followers_entry = tk.Entry(scrape_frame_4, validate='key', validatecommand=vcmd)
min_followers_entry.grid(row=0, column=1, padx=10, pady=10)

# Checkbox and input for phone country code
phone_codes_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Phone Country Codes (comma-separated)", variable=phone_codes_var).grid(row=1, column=0, padx=10, pady=10, sticky='w')
phone_codes_entry = tk.Entry(scrape_frame_4, validate='key', validatecommand=vcmd_numbers_commas)
phone_codes_entry.grid(row=1, column=1, padx=10, pady=10)

# Checkbox for biography language filter
bio_lang_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by English Biography", variable=bio_lang_var).grid(row=3, column=0, padx=10, pady=10, sticky='w')

# Checkbox and radio buttons for "Is private" filter
is_private_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Is Private", variable=is_private_var).grid(row=4, column=0, padx=10, pady=10, sticky='w')
is_private_value = tk.StringVar(value="NO")
tk.Radiobutton(scrape_frame_4, text="NO", variable=is_private_value, value="NO").grid(row=4, column=1, padx=10, pady=10, sticky='w')
tk.Radiobutton(scrape_frame_4, text="YES", variable=is_private_value, value="YES").grid(row=4, column=2, padx=10, pady=10, sticky='w')

# Checkbox and radio buttons for "Is business" filter
is_business_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Is Business", variable=is_business_var).grid(row=5, column=0, padx=10, pady=10, sticky='w')
is_business_value = tk.StringVar(value="NO")
tk.Radiobutton(scrape_frame_4, text="NO", variable=is_business_value, value="NO").grid(row=5, column=1, padx=10, pady=10, sticky='w')
tk.Radiobutton(scrape_frame_4, text="YES", variable=is_business_value, value="YES").grid(row=5, column=2, padx=10, pady=10, sticky='w')

# Checkbox and radio buttons for "Is verified" filter
is_verified_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Is Verified", variable=is_verified_var).grid(row=6, column=0, padx=10, pady=10, sticky='w')
is_verified_value = tk.StringVar(value="No")
tk.Radiobutton(scrape_frame_4, text="No", variable=is_verified_value, value="No").grid(row=6, column=1, padx=10, pady=10, sticky='w')
tk.Radiobutton(scrape_frame_4, text="Yes", variable=is_verified_value, value="Yes").grid(row=6, column=2, padx=10, pady=10, sticky='w')

# Checkbox for avatar link filter
avatar_link_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="check if have a profile pic", variable=avatar_link_var).grid(row=7, column=0, padx=10, pady=10, sticky='w')

# Checkbox for full name filter
full_name_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Full Name (not empty)", variable=full_name_var).grid(row=8, column=0, padx=10, pady=10, sticky='w')

# Checkbox and input for minimum posts count
min_posts_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Minimum Posts Count", variable=min_posts_var).grid(row=2, column=0, padx=10, pady=10, sticky='w')
min_posts_entry = tk.Entry(scrape_frame_4, validate='key', validatecommand=vcmd)
min_posts_entry.grid(row=2, column=1, padx=10, pady=10)

# Checkbox and input for biography words filter
bio_words_var = tk.BooleanVar()
tk.Checkbutton(scrape_frame_4, text="Filter by Biography Words (comma-separated)", variable=bio_words_var).grid(row=9, column=0, padx=10, pady=4, sticky='w')
bio_words_entry = tk.Entry(scrape_frame_4)
bio_words_entry.grid(row=9, column=1, padx=10, pady=4)

# Radio buttons for including or excluding biography words
include_exclude_var = tk.StringVar(value="include")
tk.Radiobutton(scrape_frame_4, text="Include specified words", variable=include_exclude_var, value="include").grid(row=10, column=0, padx=10, pady=4, sticky='w')
tk.Radiobutton(scrape_frame_4, text="Exclude specified words", variable=include_exclude_var, value="exclude").grid(row=10, column=1, padx=10, pady=4, sticky='w')



from process_the_xlsx import proces_excel_files

def apply_filters_for_all():
    apply_filters()
    email,password=get_account_for_scrape()
    if email:
     bot_name=get_user_name_and_pass()
     proces_excel_files(bot_name)
     show_current_data_for_scraper()

# Apply filters button
apply_button = tk.Button(scrape_frame_4, text="Apply Filters", command=apply_filters_for_all)
apply_button.grid(row=11, column=0, columnspan=3, pady=20)




# Create frames for each section

#  ----------

tk.Label(scrape_frame_2, text="Scrape Account", font=("Helvetica", 16)).pack(pady=10)

# Create widgets
tk.Label(scrape_frame_2, text="Email:").pack(pady=5)
email_entry_scraper = tk.Entry(scrape_frame_2, width=30)
email_entry_scraper.pack(pady=5)

tk.Label(scrape_frame_2, text="Password:").pack(pady=5)
password_entry_scraper = tk.Entry(scrape_frame_2, width=30)
password_entry_scraper.pack(pady=5)

add_button_scraper = tk.Button(scrape_frame_2, text="Add Account", command=add_account_scraper)
add_button_scraper.pack(pady=5)

# Create a Combobox
user_data_scraper = tk.StringVar()
combo_scraper = ttk.Combobox(scrape_frame_2, textvariable=user_data_scraper, state='readonly', width=30)
combo_scraper.pack(pady=10)

# Create a scrape_frame_2 for the delete and use buttons
button_frame_scraper = tk.Frame(scrape_frame_2)
button_frame_scraper.pack(pady=5)

# Add delete button
delete_button_scraper = tk.Button(button_frame_scraper, text="Delete Selected", command=delete_selected_a1_scraper)
delete_button_scraper.grid(row=0, column=0, padx=5)

# Add use button
use_button_scraper = tk.Button(button_frame_scraper, text="Use Selected", command=use_selected_1_scraper)
use_button_scraper.grid(row=0, column=1, padx=5)

# Initial data load
refresh_data_a1_scraper()

# Create for login  scraper
validate_numeric3 = button_frame_scraper.register(validate_numeric_input2)
tk.Label(button_frame_scraper, text='Sleep after login for (seconds)').grid(
    row=1, column=0, padx=5, pady=5, sticky='w')

tk.Label(button_frame_scraper, text='To get login code').grid(
    row=1, column=2, padx=1, pady=1, sticky='w')

entry_min_minute2_scrape = tk.Entry(button_frame_scraper, width=5, validate='key',
                             validatecommand=(validate_numeric3, '%d', '%P'))
entry_min_minute2_scrape.grid(row=1, column=1, padx=5, pady=5, sticky='w')

# # Create radio buttons for "use_rambler" Yes/No option
# rambler_var_scraper = tk.BooleanVar(value=True)  # Default to Yes (True)
# tk.Label(button_frame_scraper, text='Use Rambler?').grid(row=2, column=0, padx=5, pady=5, sticky='w')

# yes_button_scraper = tk.Radiobutton(button_frame_scraper, text="Yes", variable=rambler_var_scraper, value=True)
# yes_button_scraper.grid(row=2, column=1, sticky='w')

# no_button_scraper = tk.Radiobutton(button_frame_scraper, text="No", variable=rambler_var_scraper, value=False)
# no_button_scraper.grid(row=2, column=2, sticky='w')

# ________________---------------------------------


tk.Label(scrape_frame_1, text="Scrape Widget", font=("Helvetica", 12)).pack(pady=1)

# Start_scrap = tk.Button(scrape_frame_1, text="Start Scraping DM", command=start_scrape)
# Start_scrap.pack(pady=5)
# Add buttons to the scrape frame
# Add buttons to the scrape frame
download_button = tk.Button(scrape_frame_1, text="Download File", command=download_file)
download_button.pack(pady=5)

# show_button_scraper = tk.Button(scrape_frame_1, text="Show Scraped Data & History", command=show_current_data_for_scraper)
# show_button_scraper.pack(pady=5)

delete_all_button_scraper = tk.Button(scrape_frame_1, text="Delete All data & History", command=delete_all_usesrs__for_scraper)
delete_all_button_scraper.pack(pady=5)


def stop_the_app():
    import psutil

    def kill_processes_by_name(process_name):
        """
        Terminate all processes with the given name.
        """
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                print(f"Terminating process '{process_name}' with PID {proc.pid}")
                proc.kill()

    processes_to_kill = ["chromedriver.exe",]

    for process_name in processes_to_kill:
        try:
            kill_processes_by_name(process_name)
        except Exception as e:
            print(f"An error occurred while terminating {process_name}: {e}")



open_debug_button = tk.Button(GUI, text="Open Debug Window", command=open_debug_window)
open_debug_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-40)
open_debug_window()

def on_closing_1():
    # This function is called when the window is closed
    global debug_window, print_logger

    # Restore the original stdout and stderr before destroying widgets
    sys.stdout = original_stdout
    sys.stderr = original_stderr

    if debug_window is not None and debug_window.winfo_exists():
        debug_window.destroy()
        debug_window = None

    if GUI is not None:
        GUI.destroy()
        
    stop_the_app()
    
    sys.exit()

# Set up the window close handler
GUI.protocol("WM_DELETE_WINDOW", on_closing_1)

refresh_username()

# Start the Tkinter event loop
GUI.mainloop()
# ok now what 
# we are looking for a way to do this login to ask him if he has a rambler attached 


# 
# for phone verification
# //input[@placeholder="Phone number"]
# //div[@aria-label="Send code"]

#.............................................. 

# for picture profile
# //button[text()='Upload a photo']
# //div[@aria-label="Submit"]
# 
