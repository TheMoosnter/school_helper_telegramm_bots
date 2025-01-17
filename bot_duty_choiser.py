import telebot
from threading import Thread
import datetime
from config import CHAT_ID, TOKEN, STUDENT_LIST
import time
import json

bot = telebot.TeleBot(TOKEN)

print(datetime.datetime.now())
mes = {}

now_one = datetime.datetime.now()
print(f"Weekday: {now_one.weekday()}")
print(f"Hour: {now_one.hour}")
print(f"Minute: {now_one.minute}")


def update_file():
    with open("data.json", "w") as file:
        json.dump(data, file)


with open("data.json", "r") as file:
    data = json.load(file)


@bot.message_handler(commands=["start_day"])
def _new_day(message):
    new_day(data["id"])


def new_day(ind):
    global mes
    if mes:
        bot.delete_message(CHAT_ID, mes.id)
    abs_stud = ", ".join(data["absent_students"])
    mes = bot.send_message(
        CHAT_ID, f"{STUDENT_LIST[ind]} is on duty today\nMissed duty: {abs_stud}"
    )


@bot.message_handler(commands=["end"])
def _end_day(message):
    end_day()


def end_day():
    if data["a"] == 0:
        i_plus()
        check_i()
        print("id:", data["id"])
    data["a"] = 0
    print("a:", data["a"])
    update_file()


@bot.message_handler(commands=["skip"])
def skip(message):
    data["absent_students"].append(STUDENT_LIST[data["id"]])
    data["id"] += 1
    update_file()

    check_i()
    new_day(data["id"])


@bot.message_handler(commands=["put"])
def put_def(message):
    mess_text = message.text.replace("/put ", "")
    if mess_text in data["absent_students"]:
        data["a"] = STUDENT_LIST.index(mess_text)
        data["absent_students"].remove(mess_text)
        update_file()
        new_day(data["a"])
    else:
        bot.send_message(CHAT_ID, "No such person found in the list")


@bot.message_handler(commands=["set"])
def set_duty(message):
    mess_text = message.text.replace("/set ", "")
    if mess_text in STUDENT_LIST:
        data["id"] = STUDENT_LIST.index(mess_text)
        update_file()
        new_day(data["id"])
    else:
        bot.send_message(CHAT_ID, "No such person found in the list")


@bot.message_handler(commands=["skip_queue"])
def skip_without_queue(message):
    data["id"] += 1
    check_i()
    update_file()
    new_day(data["id"])


def check_i():
    if data["id"] > 10:
        data["id"] = 1
        update_file()


def i_plus():
    data["id"] += 1
    update_file()


def check_time():
    while True:
        now = datetime.datetime.now()
        if now.weekday() < 6 and now.hour == 8 and now.minute == 0 and now.second == 0:
            print(now.weekday())
            print(now.hour)
            print(now.minute)
            new_day(data["id"])
            time.sleep(60)

        elif (
            now.weekday() < 6 and now.hour == 16 and now.minute == 0 and now.second == 0
        ):
            print(now.weekday())
            print(now.hour)
            print(now.minute)
            end_day()
            time.sleep(60)
        else:
            time.sleep(60)


Thread(target=check_time, args=()).start()

bot.polling()
