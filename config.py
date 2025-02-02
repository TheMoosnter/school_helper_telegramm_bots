import os
from dotenv import load_dotenv
import csv
from loguru import logger
import yaml

def load_students(file_path):
    """
    Loads a list of students from a CSV file as a Python list.
    :param file_path: Path to CSV file.
    :return: Students' names list.
    """
    students = ['']
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row["name"])
        logger.info(f"Successfully loaded {len(students)} students from {file_path}")
    except FileNotFoundError:
        logger.error(f"File {file_path} didn't found.")
    except KeyError:
        logger.error(f"Column 'name' absent in {file_path}.")
    return students

class DataManager:
    """Handles loading, saving, and modifying data in the data.yaml file."""

    def __init__(self, file_path="data.yaml"):
        """
        Initializes the DataManager with the specified YAML file.

        :param file_path: Path to the YAML file.
        """
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """
        Loads data from the YAML file.

        :return: Dictionary containing the data from the YAML file.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}
                logger.info(f"Data successfully loaded from {self.file_path}")
                return data
        except FileNotFoundError:
            logger.error(f"File {self.file_path} not found. Creating a new one...")
            return {"id": 1, "a": 0, "absent_students": []}

    def save_data(self):
        """Saves the current data to the YAML file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(self.data, file, default_flow_style=False)
        logger.info(f"Data successfully saved to {self.file_path}")

    def get(self, key, default=None):
        """
        Retrieves a value from the data dictionary.

        :param key: The key to retrieve.
        :param default: Default value if the key is not found.
        :return: The value associated with the key or default.
        """
        return self.data.get(key, default)

    def set(self, key, value):
        """
        Updates a value in the data dictionary and saves it.

        :param key: The key to update.
        :param value: The new value.
        """
        self.data[key] = value
        self.save_data()

    def append_to_list(self, key, value):
        """
        Appends a value to a list in the data dictionary.

        :param key: The key of the list.
        :param value: The value to append.
        """
        self.data[key].append(value)
        self.save_data()

    def remove_from_list(self, key, value):
        """
        Removes a value from a list in the data dictionary.

        :param key: The key of the list.
        :param value: The value to remove.
        """
        if key in self.data and value in self.data[key]:
            self.data[key].remove(value)
            self.save_data()

# Configure logging
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger.add(LOG_FILE, rotation="10 MB", level="INFO", format="{time} {level} {message}")

# Load data from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# File for saving program variables
DATA_FILE = "data.yaml"

# Loading of student list from .cvs file to list constant
STUDENT_LIST = load_students("students.csv")
