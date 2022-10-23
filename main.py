import logging.config
import re

import corp_model
import sql
from sql import employee_search

from telebot import types, TeleBot

from config import config

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


def get_args(msg: types.Message) -> str:
    return " ".join(msg.text.split()[1:]) if len(msg.text.split()) > 1 else None


@bot.message_handler(commands=['start'])
def start_message(message):
    reply(message, "Привет ✌")


def print_employee(empl: corp_model.Employee) -> str:
    _text = f"""Нашел:
{empl.last_name} {empl.first_name}
email: {empl.email}
tel: {empl.internal_phone}
mobile: {empl.external_phone}"""
    return _text


@bot.message_handler(commands=['найди', 'find'])
def button_message(message):
    _name = get_args(message)
    if re.match(r'^[\w\-_@ ]*$', _name):
        reply(message, f"Начинаю искать {_name}")
        _employes = sql.employee_search(_name)
        if len(_employes) == 1:
            for e in _employes:
                reply(message, print_employee(e))
        else:
            markup = types.InlineKeyboardMarkup()
            for e in _employes:
                markup.add(types.InlineKeyboardButton(
                    text=e.name,
                    callback_data=f"employee {e.id}"
                ))
            bot.send_message(
                chat_id=message.chat.id,
                text="Вот что я нашел:",
                reply_markup=markup,
                parse_mode='HTML'
            )
    else:
        reply(message, f"Странные у вас имена. Попробуйте попроще. {_name}")


if __name__ == "__main__":
    bot.send_message(129384888, "Starting")
    bot.infinity_polling()
