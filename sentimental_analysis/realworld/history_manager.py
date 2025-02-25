import json
from django.contrib.auth import get_user
import os
from datetime import datetime

# Define the directory path
directory_path = os.path.join("sentimental_analysis", "media", "user_data")


def create_storage(username):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Create a JSON file with the username and save data along with timestamp
    file_path = os.path.join(directory_path, f"{username}.json")

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file does not exist, create an empty dictionary
        with open(file_path, 'w') as json_file:
            json.dump({
                "Product_Analysis": {},
                "Image_Analysis": {},
                "News_Analysis": {},
                "Live_Speech": {},
                "Text_Analysis": {},
                "Batch_Analysis": {},
                "Doc_Analysis": {},
                "Audio_Analysis": {},
                "Facebook": {},
                "Twitter": {},
                "Reddit": {},
            }, json_file)


def store_text_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Text Analysis" section with the new data
    if "Text_Analysis" not in existing_data:
        existing_data["Text_Analysis"] = {}
    existing_data["Text_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

def store_image_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Image Analysis" section with the new data
    if "Image_Analysis" not in existing_data:
        existing_data["Image_Analysis"] = {}
    existing_data["Image_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

def store_news_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "News Analysis" section with the new data
    if "News_Analysis" not in existing_data:
        existing_data["News_Analysis"] = {}
    existing_data["News_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)