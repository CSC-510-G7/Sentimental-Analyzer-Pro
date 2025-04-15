import sys
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
import json

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Assuming the functions are in a module named `history_manager`
from sentimental_analysis.realworld.history_manager import (
    create_storage,
    store_text_analysis,
    store_image_analysis,
    store_news_analysis,
    store_batch_analysis,
    store_document_analysis,
    store_audio_analysis,
    store_live_analysis,
    store_facebook_data,
    store_twitter_data,
    store_reddit_data,
    store_product_analysis
)

class TestCreateStorage(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.os.path.exists')
    @patch('sentimental_analysis.realworld.history_manager.os.makedirs')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_create_storage(self, mock_json_dump, mock_open, mock_makedirs, mock_path_exists):
        # Setup
        username = 'testuser'
        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{username}.json")

        # Mock responses
        mock_path_exists.side_effect = lambda path: path != directory_path and path != file_path

        # Call the function
        create_storage(username)

        # Assertions
        mock_makedirs.assert_called_once_with(directory_path)
        mock_open.assert_called_once_with(file_path, 'w')
        mock_json_dump.assert_called_once_with({
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
            "Youtube": {},
        }, mock_open())

class TestStoreTextAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_text_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_text_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Text_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

class TestStoreImageAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_image_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_image_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Image_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreNewsAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_news_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_news_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["News_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreBatchAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_batch_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_batch_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Batch_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreDocumentAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_document_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_document_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Doc_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreAudioAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_audio_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_audio_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Audio_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreLiveAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_live_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_live_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Live_Speech"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_live_analysis_anonymous_user(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Nominal scenario: Anonymous user
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = False
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, "Anonymous.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_live_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with("Anonymous")
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Live_Speech"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)
# Repeat similar test cases for other functions

class TestStoreFacebookData(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_facebook_data(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_facebook_data(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Facebook"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_facebook_data_anonymous_user(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Nominal scenario: Anonymous user
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = False
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, "Anonymous.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_facebook_data(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with("Anonymous")
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Facebook"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreTwitterData(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_twitter_data(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_twitter_data(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Twitter"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_twitter_data_anonymous_user(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Nominal scenario: Anonymous user
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = False
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, "Anonymous.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_twitter_data(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with("Anonymous")
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Twitter"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

# Repeat similar test cases for other functions

class TestStoreRedditData(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_reddit_data(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_reddit_data(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Reddit"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_reddit_data_anonymous_user(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Nominal scenario: Anonymous user
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = False
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, "Anonymous.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_reddit_data(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with("Anonymous")
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Reddit"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)


# Repeat similar test cases for other functions

class TestStoreProductAnalysis(unittest.TestCase):

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_product_analysis(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Setup
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_product_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with(user.username)
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Product_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_product_analysis_anonymous_user(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Nominal scenario: Anonymous user
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = False
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, "Anonymous.json")

        # Mock existing data
        existing_data = {
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
        }
        mock_json_load.return_value = existing_data

        # Call the function
        store_product_analysis(request, data)

        # Assertions
        mock_create_storage.assert_called_once_with("Anonymous")
        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()
        
        # Check if the data was updated correctly
        updated_data = existing_data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_data["Product_Analysis"][timestamp] = data
        mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_product_analysis_missing_directory(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Off-nominal scenario: Missing directory
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock os.path.exists to simulate missing directory
        with patch('sentimental_analysis.realworld.history_manager.os.path.exists', return_value=False):
            # Call the function
            store_product_analysis(request, data)

            # Assertions
            mock_create_storage.assert_called_once_with(user.username)
            mock_open.assert_any_call(file_path, 'r')
            mock_open.assert_any_call(file_path, 'w')
            mock_json_load.assert_called_once()
            mock_json_dump.assert_called_once()
            

    # @patch('sentimental_analysis.realworld.history_manager.get_user')
    # @patch('sentimental_analysis.realworld.history_manager.create_storage')
    # @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    # @patch('sentimental_analysis.realworld.history_manager.json.load')
    # @patch('sentimental_analysis.realworld.history_manager.json.dump')
    # def test_store_product_analysis_invalid_json(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
    #     # Off-nominal scenario: Invalid JSON data
    #     request = MagicMock()
    #     data = {"key": "value"}
    #     user = MagicMock()
    #     user.is_authenticated = True
    #     user.username = 'testuser'
    #     mock_get_user.return_value = user

    #     directory_path = os.path.join("sentimental_analysis", "media", "user_data")
    #     file_path = os.path.join(directory_path, f"{user.username}.json")

    #     # Mock json.load to raise a JSONDecodeError
    #     mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

    #     # Call the function
    #     store_product_analysis(request, data)

    #     # Assertions
    #     mock_create_storage.assert_called_once_with(user.username)
    #     mock_open.assert_any_call(file_path, 'r')
    #     mock_open.assert_any_call(file_path, 'w')
    #     mock_json_load.assert_called_once()
    #     mock_json_dump.assert_called_once()
        
    #     # Check if the data was updated correctly
    #     updated_data = {
    #         "Product_Analysis": {},
    #         "Image_Analysis": {},
    #         "News_Analysis": {},
    #         "Live_Speech": {},
    #         "Text_Analysis": {},
    #         "Batch_Analysis": {},
    #         "Doc_Analysis": {},
    #         "Audio_Analysis": {},
    #         "Facebook": {},
    #         "Twitter": {},
    #         "Reddit": {},
    #     }
    #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     updated_data["Product_Analysis"][timestamp] = data
    #     mock_json_dump.assert_called_once_with(updated_data, mock_open(), indent=4)

    @patch('sentimental_analysis.realworld.history_manager.get_user')
    @patch('sentimental_analysis.realworld.history_manager.create_storage')
    @patch('sentimental_analysis.realworld.history_manager.open', new_callable=mock_open)
    @patch('sentimental_analysis.realworld.history_manager.json.load')
    @patch('sentimental_analysis.realworld.history_manager.json.dump')
    def test_store_product_analysis_permission_error(self, mock_json_dump, mock_json_load, mock_open, mock_create_storage, mock_get_user):
        # Off-nominal scenario: File permission error
        request = MagicMock()
        data = {"key": "value"}
        user = MagicMock()
        user.is_authenticated = True
        user.username = 'testuser'
        mock_get_user.return_value = user

        directory_path = os.path.join("sentimental_analysis", "media", "user_data")
        file_path = os.path.join(directory_path, f"{user.username}.json")

        # Mock open to raise a PermissionError
        mock_open.side_effect = PermissionError

        # Call the function and assert that it raises a PermissionError
        with self.assertRaises(PermissionError):
            store_product_analysis(request, data)

if __name__ == '__main__':
    unittest.main()