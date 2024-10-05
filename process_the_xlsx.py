# programed By Mohamed Hafez : phone number >> +201552990073 works for whatsUP and telegram
import os
import pandas as pd
from langdetect import detect, LangDetectException
import json

def proces_excel_files(bot_name):
    current_directory = os.getcwd().replace('\\','/') + '/'
    download_directory = f"{current_directory}Downloads".replace('/','\\')
    input_folder=download_directory
    output_folder = r'data'
    output_file = f'data_{bot_name}_.csv'     

    all_files = os.listdir(input_folder)

    ig_files = [file for file in all_files if file.startswith(
        'ig-') and file.endswith('.xlsx')]


    if not ig_files:
        print("No matching files found.")


    merged_data = pd.DataFrame()

    for file in ig_files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_excel(file_path)
        merged_data = pd.concat([merged_data, df], ignore_index=True)

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, output_file)
    merged_data.to_csv(output_path, index=False)

    print(f"Merged data from {len(ig_files)} files into {output_path}.")
    try:
     delete_files(input_folder)
    except Exception as e :
        print(e)
    try:
     merge_full_with_new(bot_name)
    except Exception as e :
        print(e)
    try:
     apply_filters(bot_name)
    except Exception as e :
        print(e)

def delete_files(input_folder):

    all_files = os.listdir(input_folder)
    ig_files = [file for file in all_files if file.startswith(
        'ig-') and file.endswith('.xlsx')]

    if not ig_files:
        print("No matching files found.")
        return
    
    for file in ig_files:
        file_path = os.path.join(input_folder, file)
        os.remove(file_path)
        print(f"Deleted file: {file_path}")


def merge_full_with_new(bot_name):
    full_data_path = f"data/full_data_{bot_name}_.csv"
    new_data_path = f'data/data_{bot_name}_.csv'
    
    header_line = "Instagram ID,Username,Full name,Profile link,Avatar pic,Followed by viewer,Is verified,Followers count,Following count,Biography,Public email,Posts count,Phone country code,Phone number,City,Address,Is private,Is business,External url\n"

    # Check if the file exists, if not, create it and write the header
    def funcoto(full_datapatho):
     if not os.path.exists(full_datapatho):
        with open(full_datapatho, 'w',encoding='utf-8') as f:
            f.write(header_line)
            print(f"Created new file: {full_datapatho}")
     else:
        print(f"File already exists: {full_datapatho}")
    
    funcoto(full_data_path)
    funcoto(new_data_path)
    
    existing_data = pd.read_csv(full_data_path)

    new_data = pd.read_csv(new_data_path)

    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    existing_data = combined_data

    existing_data.to_csv(full_data_path, index=False)

def filter_data(bot_name, apply_phone_codes, phone_codes, apply_min_followers, min_followers, apply_bio_lang, apply_is_private, is_private, apply_is_business, is_business, apply_is_verified, is_verified, apply_avatar_link, apply_full_name, apply_min_posts, min_posts,apply_bio_words, bio_words, exclude_bio_words):
    input_file_path = os.path.join('data', f'full_data_{bot_name}_.csv')
    if input_file_path:
        print(input_file_path)
    df = pd.read_csv(input_file_path)

   
    if apply_min_followers and not df.empty:
        # Filter by minimum followers count
        df = df[pd.to_numeric(df['Followers count'], errors='coerce').fillna(0) > min_followers]
 
    
    
    if apply_phone_codes and not df.empty:
        # Filter by phone country code if provided
        df = df[df['Phone country code'].isin(phone_codes)]
    
    
    if apply_bio_lang and not df.empty:
        def is_english(bio):
            try:
                return detect(bio) == 'en'
            except LangDetectException:
                return False

        # Filter by English biography
        df = df[df['Biography'].apply(lambda bio: is_english(bio) if pd.notnull(bio) else False)]
    
    
    if apply_is_private and not df.empty:
        # Filter by "Is private" column
        df = df[df['Is private'] == is_private]
    
    
    if apply_is_business and not df.empty:
        # Filter by "Is business" column
        df = df[df['Is business'] == is_business]
    
    
    if apply_is_verified and not df.empty:
        # Filter by "Is verified" column
        df = df[df['Is verified'] == is_verified]
    
    
    if apply_avatar_link and not df.empty:
        # Filter by "Avatar pic" column
        df = df[df['Avatar pic'].apply(lambda link: link.startswith("https://instagram.") if pd.notnull(link) else False)]
    
    
    if apply_full_name and not df.empty:
        # Filter by whether "Full name" column has a value
        df = df[pd.notnull(df['Full name']) & df['Full name'].str.strip().astype(bool)]
    
    
    if apply_min_posts and not df.empty:
        # Filter by minimum posts count
        df = df[pd.to_numeric(df['Posts count'], errors='coerce').fillna(0) >= min_posts]

    
    if apply_bio_words and not df.empty:
        # Filter by specified words in username, biography, or full name
        bio_words_list = [word.strip().lower() for word in bio_words.split(',')]
        if exclude_bio_words:
            df = df[~df['Biography'].apply(lambda bio: any(word in bio.lower() for word in bio_words_list) if pd.notnull(bio) else False) &
                    ~df['Full name'].apply(lambda name: any(word in name.lower() for word in bio_words_list) if pd.notnull(name) else False) &
                    ~df['Username'].apply(lambda username: any(word in username.lower() for word in bio_words_list) if pd.notnull(username) else False)]
        else:
            df = df[df['Biography'].apply(lambda bio: any(word in bio.lower() for word in bio_words_list) if pd.notnull(bio) else False) |
                    df['Full name'].apply(lambda name: any(word in name.lower() for word in bio_words_list) if pd.notnull(name) else False) |
                    df['Username'].apply(lambda username: any(word in username.lower() for word in bio_words_list) if pd.notnull(username) else False)]
 
    df = df[['Username', 'Full name', 'Phone country code', 'Phone number', 'Followers count', 'Is private', 'Is business', 'Is verified']]
    df = df.drop_duplicates()

    output_file_path = os.path.join('scrape', f'filtered_data_{bot_name}_.csv')
    df.to_csv(output_file_path, index=False)
    print(f"Filtered and de-duplicated data has been saved to {output_file_path}_")

def copy_and_deduplicate(bot_name):
    # File paths
    source_file = f'scrape/filtered_data_{bot_name}_.csv'
    destination_file = f'needs/users_to_reach_{bot_name}_.csv'

    # Read the source file and get the first two columns
    df_source = pd.read_csv(source_file, usecols=[0, 1])

    # If destination file exists, read it and append new data
    if os.path.exists(destination_file):
        df_destination = pd.read_csv(destination_file)
        df_combined = pd.concat([df_destination, df_source])
    else:
        df_combined = df_source

    # Drop duplicates
    df_combined.drop_duplicates(inplace=True)

    # Save the deduplicated data to the destination file
    df_combined.to_csv(destination_file, index=False)
def apply_filters(bot_name):

    settings = load_settings(bot_name)

    apply_phone_codes = settings.get("apply_phone_codes", False)
    phone_codes = [int(code.strip()) for code in settings.get("phone_codes", "").split(',')] if settings.get("phone_codes") else []

    apply_min_followers = settings.get("apply_min_followers", False)
    try:
     min_followers = int(settings.get("min_followers", "0"))
    except :
        min_followers=0

    apply_bio_lang = settings.get("apply_bio_lang", False)

    apply_is_private = settings.get("apply_is_private", False)
    is_private = settings.get("is_private", "NO")

    apply_is_business = settings.get("apply_is_business", False)
    is_business = settings.get("is_business", "NO")

    apply_is_verified = settings.get("apply_is_verified", False)
    is_verified = settings.get("is_verified", "No")

    apply_avatar_link = settings.get("apply_avatar_link", False)

    apply_full_name = settings.get("apply_full_name", False)

    apply_min_posts = settings.get("apply_min_posts", False)
    try:
     min_posts = int(settings.get("min_posts", "1"))
    except :
        min_posts=1

    apply_bio_words =settings.get("apply_bio_words", False)
    bio_words = settings.get("bio_words", "")
    include_exclude=settings.get("include_exclude", "include")

    filter_data(bot_name, apply_phone_codes, phone_codes, apply_min_followers, min_followers, apply_bio_lang, apply_is_private, is_private, apply_is_business, is_business, apply_is_verified, is_verified, apply_avatar_link, apply_full_name, apply_min_posts, min_posts,apply_bio_words, bio_words, include_exclude == "exclude")
    copy_and_deduplicate(bot_name)

def load_settings(bot_name):
    try:
        with open(f'scrape/filter_settings_{bot_name}_.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

