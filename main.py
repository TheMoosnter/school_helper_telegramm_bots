import time
from threading import Thread
from loguru import logger
from telebot import TeleBot
from config import TOKEN, CHAT_ID, DATA_FILE
from utils import DutyBot

def main():
    """
    Entry point to the application. Initializes the bot and starts the main processes.
    """
    logger.info("Запуск телеграм-бота")
    bot = TeleBot(TOKEN)
    duty_bot = DutyBot(bot, CHAT_ID)

    # Command handlers
    @bot.message_handler(commands = ['start_day'])
    def _start_day(message):
        duty_bot.new_day()

    @bot.message_handler(commands=['end_day'])
    def _start_day(message):
        duty_bot.end_day()

    # Start a background thread to check the time
    #Thread(target=duty_bot.check_time).start()

    # Bot start
    bot.polling()


if __name__ == "__main__":
    main()

