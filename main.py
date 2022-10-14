import ast
import json
import logging
import logging.config
import re
from idlelib.query import Query

from telebot import types, TeleBot
from corp_model import Employee

from config import config
from sql import db_session

tg_config = config['telegram']
bot = TeleBot(tg_config['token'])

if "logging" in config.keys():
    logging.config.dictConfig(config["logging"])
else:
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
crossIcon = u"\u274C"


def reply(msg: types.Message, text):
    log.info(f"Chat: {msg.chat.id} user: {msg.from_user.username} text: [{msg.text}]")
    bot.send_message(msg.chat.id, text)


def get_args(msg: types.Message)-> str:
    return " ".join(msg.text.split()[1:]) if len(msg.text.split()) > 1 else None


def find_employee(search_str: str) -> list[str]:
    _search = db_session.query(Employee).filter(Employee.first_name.ilike(f"%{search_str}%"))

@bot.message_handler(commands=['start'])
def start_message(message):
    reply(message, "Привет ✌")


@bot.message_handler(commands=['найди', 'find'])
def button_message(message):
    _name = get_args(message)
    if re.match(r'^[\w\-_@ ]*$', _name):
        reply(message, f"Начинаю искать {_name}")
        _search = db_session.query(Employee).filter(Employee.first_name.ilike(f"%{_name}%")).first()
        reply(message, f"Нашел: {_search}")
    else:
        reply(message, f"Странные у вас имена. Попробуйте попроще. {_name}")


if __name__ == "__main__":
    bot.send_message(129384888, "Starting")
    bot.infinity_polling()
