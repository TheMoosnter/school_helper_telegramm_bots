import datetime
import asyncio

from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


from config import CHAT_ID, STUDENT_LIST, TOKEN, DataManager
from utils import DutyBot


logger.info("Launching a telegram bot")
now_one = datetime.datetime.now()
logger.info(f"Hours: {now_one.hour}, minutes: {now_one.minute}")

bot = Bot(token=str(TOKEN))
dp = Dispatcher()
data_manager = DataManager()
duty_bot = DutyBot(bot, CHAT_ID, STUDENT_LIST, data_manager)

scheduler = AsyncIOScheduler()

scheduler.add_job(
    duty_bot.time_duty_set, CronTrigger(day_of_week="mon-fri", hour=8, minute=0)
)


# Command handlers
@dp.message(Command("start_day"))
async def _start_day(message: Message):
    await duty_bot.new_day()


@dp.message(Command("end_day"))
async def _end_day(message: Message):
    await duty_bot.end_day()


@dp.message(Command("skip"))
async def skip(message: Message):
    """
    Adds the current duty officer to the absent list and moves on to the next one.
    """
    await duty_bot.process_skip()


@dp.message(Command("put"))
async def put(message: Message):
    """
    Place the missing student on duty.
    Command format: /put <Student_name>.
    """
    student_name = message.text.replace("/put ", "").strip()
    await duty_bot.process_put(student_name, message.chat.id)


@dp.message(Command("set"))
async def set_duty(message: Message):
    """
    Set a specific student as the on-duty student.
    Command format: /set <Student_name>.
    """
    student_name = message.text.replace("/set ", "").strip()
    await duty_bot.process_set(student_name, message.chat.id)


@dp.message(Command("skip_queue"))
async def skip_without_queue(message: Message):
    """
    Skip the current duty without taking into account his absence.
    """
    await duty_bot.skip_queue()


# Start a background thread to check the time
# Thread(target=duty_bot.check_time).start()


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN)
    scheduler.start()
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
