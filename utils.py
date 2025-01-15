import os
import time
import datetime
import yaml
from loguru import logger
from config import DATA_FILE, STUDENT_LIST

class DutyBot:

    def __init__(self, bot, chat_id):
        """
        Initialization of DutyBot.

        :param bot: Object TeleBot.
        :param chat_id: Chat ID to send messages to.
        """
        self.bot = bot
        self.chat_id = chat_id
        self.data = self.load_data()
        self.mes = None

    def load_data(self):
        """
        Load data from the YAML file.

        :return: Duty's data.
        """
        if not os.path.exists(DATA_FILE):
            logger.warning("Файл данных не найден. Создается новый.")
            return {"id": 0, "a": 0, "absent_students": []}
        with open(DATA_FILE, "r") as file:
            return yaml.safe_load(file)

    def save_data(self):
        """
        Save data in the YAML file.
        """
        with open(DATA_FILE, "w") as file:
            yaml.safe_dump(self.data, file)
        logger.debug("Данные сохранены")

    def new_day(self, student_index = None):
        """
        Updates information about the person on duty for the new day.
        """

        student_index = student_index if student_index is not None else self.data["id"]
        abs_stud = ", ".join(self.data["absent_students"])
        self.mes = self.bot.send_message(self.chat_id, f'{STUDENT_LIST[student_index]} is on duty today\nMissed duty: {abs_stud}')

    def end_day(self):
        """
        Ends the current duty day and updates the counter.
        """
        if self.data["a"] == 0:
            self.increment_id()
            self.check_id()
        self.data["a"] = 0
        self.save_data()

    def increment_id(self):
        """
        Increments the ID of the current duty officer.
        """
        self.data["id"] += 1

    def check_id(self):
        """
        Checks if the identifier is greater than the number of students.
        """
        if self.data["id"] >= len(STUDENT_LIST):
            self.data["id"] = 0