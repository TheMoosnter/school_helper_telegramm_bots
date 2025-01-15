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
            return {"id": 1, "a": 0, "absent_students": []}
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
            self.data["id"] = 1


    def process_skip(self):
        """
        Adds the current duty officer to the absent list and moves on to the next one.
        """
        if self.mes:
            self.bot.delete_message(self.chat_id, self.mes.id)
        self.data["absent_students"].append(STUDENT_LIST[self.data["id"]])
        self.increment_id()
        self.check_id()
        self.save_data()
        self.new_day()

    def process_put(self, student_name):
        """
        Sets the missing student as the duty.

        :param student_name: Student name.
        """
        if student_name in self.data["absent_students"]:
            if self.mes:
                self.bot.delete_message(self.chat_id, self.mes.id)
            self.data["a"] = STUDENT_LIST.index(student_name)
            self.data["absent_students"].remove(student_name)
            self.save_data()
            self.new_day(self.data["a"])
        else:
            self.bot.send_message(self.chat_id, "No such person found in the list")

    def process_set(self, student_name):
        """
        Sets the specified student as the on-duty student.

        :param student_name: Student name.
        """
        if student_name in STUDENT_LIST:
            if self.mes:
                self.bot.delete_message(self.chat_id, self.mes.id)
            self.data["id"] = STUDENT_LIST.index(student_name)
            self.save_data()
            self.new_day()
        else:
            self.bot.send_message(self.chat_id, "No such person found in the list")

    def skip_queue(self):
        """
        Allows the current person on duty to pass without taking into account their absence.
        """
        if self.mes:
            self.bot.delete_message(self.chat_id, self.mes.id)
        self.increment_id()
        self.check_id()
        self.save_data()
        self.new_day()

    def check_time(self):
        """
        Background task for checking time. Updates the duty officer every day at 8:00.
        """
        while True:
            now = datetime.datetime.now()
            if now.weekday() < 6 and now.hour == 8 and now.minute == 0:
                logger.info("Обновление дежурного дня")
                self.end_day()
                self.new_day()
                time.sleep(60)
            else:
                time.sleep(59)