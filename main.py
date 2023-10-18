import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

import datetime
import logging


Logger = logging.getLogger("info")
logging.basicConfig(filename=f'log_{datetime.datetime.now()}.txt', filemode='w', level=logging.INFO)


state_storage = StateMemoryStorage()
# Вставить свой токен или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6394285783:AAH4_fnb0JEInznJ0-2iV38PfZWXWSImkjE",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    register_name = State()
    register_age = State()
    login = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация/Логин"  # Можно менять текст
text_button_1 = "САМОЕ КРУТОЕ ВИДЕО НА ЗЕМЛЕ"  # Можно менять текст
text_button_2 = "Кнопка 2"  # Можно менять текст
text_button_3 = "Кнопка 3"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Что будем делать?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.register_name, message.chat.id)


@bot.message_handler(state=PollState.register_name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! [Ваш](https://www.example.com/) возраст?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.register_age, message.chat.id)


@bot.message_handler(state=PollState.register_age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
        bot.send_message(message.chat.id, f'Спасибо за регистрацию, {data["name"]}!', reply_markup=menu_keyboard)
    bot.set_state(message.from_user.id, PollState.login, message.chat.id)


@bot.message_handler(state=PollState.login)
def menu(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.send_message(message.chat.id, f'Приветствую тебя, {data["name"]}')


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Вот [Видео](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", reply_markup=menu_keyboard, disable_web_page_preview=True)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Текст 2", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Текст 3", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()