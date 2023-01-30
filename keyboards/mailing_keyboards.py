from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_add_button = ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
kb_add_button.add(KeyboardButton('Да, добавить кнопку'))
kb_add_button.add(KeyboardButton('Нет, продолжить'))