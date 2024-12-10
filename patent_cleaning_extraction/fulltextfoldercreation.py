import os
import shutil

# Define the folder containing the files
folder_path = "fulltextrawdata2023"

# Iterate over all items in the folder
for item in os.listdir(folder_path):

    item_path = os.path.join(folder_path, item)
    
    # Check if the item is a file and has a .xml extension
    if os.path.isfile(item_path) and item.endswith('.xml'):
        # Create a folder with the same name as the XML file (without extension)
        folder_name = os.path.splitext(item)[0]
        folder_path_new = os.path.join(folder_path, folder_name)
        
        # Ensure the folder does not already exist
        if not os.path.exists(folder_path_new):
            os.makedirs(folder_path_new)
        
        # Move the XML file into the newly created folder
        shutil.move(item_path, os.path.join(folder_path_new, item))