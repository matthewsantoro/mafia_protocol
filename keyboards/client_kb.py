from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/autor')
b2 = KeyboardButton('/start')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)


kb_client.add(b1).insert(b2)