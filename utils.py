import time
import datetime
from loguru import logger


class DutyBot:
    def __init__(self, bot, chat_id, student_list, data_manager):
        """
        Initialization of DutyBot.

        :param bot: Object TeleBot.
        :param chat_id: Chat ID to send messages to.
        """
        self.bot = bot
        self.chat_id = chat_id
        self.student_list = student_list
        self.data_manager = data_manager
        self.mes = None

    def check_student_in_list(self, student, list):
        """
        Checks if a student exists in the given list.

        :param student: Name of the student to check.
        :param list: List in which exist of the student is checked
        :return: True if the student exists, False otherwise.
        """
        return student in list

    def new_day(self, student_index=None):
        """
        Updates information about the person on duty for the new day.
        """

        student_index = student_index if student_index is not None else self.data_manager.get("id", 0)
        abs_stud = ", ".join(self.data_manager.get("absent_students", []))
        self.mes = self.bot.send_message(
            self.chat_id,
            f"{self.student_list[student_index]} is on duty today\nMissed duty: {abs_stud}",
        )
        logger.info(f"New duty selected: {self.student_list[student_index]}")

    def end_day(self):
        """
        Ends the current duty day and updates the counter.
        """
        if self.data_manager.get("a") == 0:
            self.increment_id()
            self.check_id()
        self.data_manager.set("a", 0)

    def increment_id(self):
        """
        Increments the ID of the current duty officer.
        """
        self.data_manager.set("id", self.data_manager.get("id", 0) + 1)

    def check_id(self):
        """
        Checks if the identifier is greater than the number of students.
        """
        if self.data_manager.get("id") >= len(self.student_list):
            self.data_manager.set("id", 1)
            logger.info("Student list was started anew.")

    def process_skip(self):
        """
        Adds the current duty officer to the absent list and moves on to the next one.
        """
        if self.mes:
            self.bot.delete_message(self.chat_id, self.mes.id)
        logger.info(f"Student {self.student_list[self.data_manager.get("id", 0)]} was marked as absent.")
        self.data_manager.append_to_list("absent_students", self.student_list[self.data_manager.get("id", 0)])
        self.increment_id()
        self.check_id()
        self.new_day()

    def process_put(self, student_name, personal_mes_chat_id):
        """
        Sets the missing student as the duty.

        :param student_name: Student name.
        :param student_name: Author chat id (for send error message)
        """
        absent_students = self.data_manager.get("absent_students", [])
        if self.check_student_in_list(student_name, absent_students):
            if self.mes:
                self.bot.delete_message(self.chat_id, self.mes.id)
            logger.info("The absent student was appointed on duty.")
            self.data_manager.set("a", self.student_list.index(student_name))
            self.data_manager.remove_from_list("absent_students", student_name)
            self.new_day(self.data_manager.get("a"))
        else:
            self.bot.send_message(personal_mes_chat_id, "No such person found in the list")

    def process_set(self, student_name, personal_mes_chat_id):
        """
        Sets the specified student as the on-duty student.

        :param student_name: Student name.
        """
        if self.check_student_in_list(student_name, self.student_list):
            if self.mes:
                self.bot.delete_message(self.chat_id, self.mes.id)
            logger.info("The student was appointed on duty manually.")
            self.data_manager.set("id", self.student_list.index(student_name))
            self.new_day(self.data_manager.get("id"))
        else:
            self.bot.send_message(personal_mes_chat_id, "No such person found in the list")

    def skip_queue(self):
        """
        Allows the current person on duty to pass without taking into account their absence.
        """
        if self.mes:
            self.bot.delete_message(self.chat_id, self.mes.id)
        logger.info("The student skipped his duty.")
        self.increment_id()
        self.check_id()
        self.new_day()

    def check_time(self):
        """
        Background task for checking time. Updates the duty officer every day at 8:00.
        """
        while True:
            now = datetime.datetime.now()
            if now.weekday() < 6 and now.hour == 23 and now.minute == 10:
                logger.info("Day duty update")
                self.end_day()
                self.new_day()
                time.sleep(60)
            else:
                time.sleep(59)
