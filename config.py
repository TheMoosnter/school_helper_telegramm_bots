import os
from dotenv import load_dotenv
import csv
from loguru import logger

load_dotenv()

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

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DATA_FILE = "data.yaml"

STUDENT_LIST = load_students("students.csv")
