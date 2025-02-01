from threading import Thread
from loguru import logger
from telebot import TeleBot
from config import TOKEN, CHAT_ID, DataManager
from utils import DutyBot
import datetime


def main():
    """
    Entry point to the application. Initializes the bot and starts the main processes.
    """
    logger.info("Launching a telegram bot")
    now_one = datetime.datetime.now()
    logger.info(f"Hours: {now_one.hour}, minutes: {now_one.minute}")
    bot = TeleBot(TOKEN)
    data_manager = DataManager()
    duty_bot = DutyBot(bot, CHAT_ID, data_manager)

    # Command handlers
    @bot.message_handler(commands=["start_day"])
    def _start_day(message):
        duty_bot.new_day()

    @bot.message_handler(commands=["end_day"])
    def _end_day(message):
        duty_bot.end_day()

    @bot.message_handler(commands=["skip"])
    def skip(message):
        """
        Adds the current duty officer to the absent list and moves on to the next one.
        """
        duty_bot.process_skip()

    @bot.message_handler(commands=["put"])
    def put(message):
        """
        Place the missing student on duty.
        Command format: /put <Student_name>.
        """
        student_name = message.text.replace("/put ", "").strip()
        duty_bot.process_put(student_name)

    @bot.message_handler(commands=["set"])
    def set_duty(message):
        """
        Set a specific student as the on-duty student.
        Command format: /set <Student_name>.
        """
        student_name = message.text.replace("/set ", "").strip()
        duty_bot.process_set(student_name)

    @bot.message_handler(commands=["skip_queue"])
    def skip_without_queue(message):
        """
        Skip the current duty without taking into account his absence.
        """
        duty_bot.skip_queue()

    # Start a background thread to check the time
    Thread(target=duty_bot.check_time).start()

    # Bot start
    bot.polling()


if __name__ == "__main__":
    main()
