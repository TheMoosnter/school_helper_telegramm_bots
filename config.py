import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DATA_FILE = "data.yaml"

STUDENT_LIST = [
    "",
    "Tom",
    "Bob",
    "Mary",
    "Patrick",
    "John",
    "Angela",
    "Jacob",
    "Olivia",
    "Michael",
    "Sophia",
]
