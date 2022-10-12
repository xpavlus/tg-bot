import ast
import json
import logging
import logging.config
import os.path

import telebot.types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import types, TeleBot
from corp_model import Employee

default_config_path = "./config.json"
if os.path.isfile(default_config_path):
    with open(default_config_path, 'r') as f:
        config = json.load(f)

bot = TeleBot(config['telegram']['token'])


if "logging" in config.keys():
    logging.config.dictConfig(config["logging"])
else:
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

sql_connector = "%(engine)s+%(driver)s://%(db_user)s:%(db_password)s@%(host)s:%(port)s/%(database)s"\
                % config["database"]
_engine = create_engine(sql_connector)
_session = sessionmaker(bind=_engine)
db_session = _session()

stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
crossIcon = u"\u274C"


def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
                   types.InlineKeyboardButton(text=crossIcon,
                                              callback_data="['key', '" + key + "']"))

    return markup


def reply(msg: telebot.types.Message, text):
    log.info(f"Chat: {msg.chat.id} user: {msg.from_user.username} text: [{msg.text}]")
    bot.send_message(msg.chat.id, text)


def get_args(msg: telebot.types.Message):
    return msg.text.split()[1:] if len(msg.text.split()) > 1 else None


@bot.message_handler(commands=['test'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the values of stringList",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start_message(message):
    reply(message, "Привет ✌")


@bot.message_handler(commands=['найди', 'find'])
def button_message(message):
    reply(message, f"Начинаю искать {get_args(message)}")


@bot.message_handler(commands=['stop', 'exit'])
def on_stop(message):
    reply(message, "Ok Exiting 🛑")
    logging.info("Correct exit.")
    bot.stop_polling()


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data.startswith("['value'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode='HTML')


if __name__ == "__main__":
    bot.send_message(129384888, "Starting")
    bot.infinity_polling()
