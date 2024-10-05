import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'data' folder relative to the script's directory
data_folder_path = os.path.join(script_dir, 'data')

# List the contents of the 'data' folder
data_contents = os.listdir(data_folder_path)

print(data_contents)


import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
