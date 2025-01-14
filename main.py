import telebot
from threading import Thread
import datetime
from config import CHAT_ID, TOKEN, STUDENT_LIST
import time
import json


bot = telebot.TeleBot(TOKEN)
