from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

vote_button = KeyboardButton('Никто не покинул')
kb_vote = ReplyKeyboardMarkup(resize_keyboard=True)
kb_vote.add(vote_button)
murder_button = KeyboardButton('Промах')
kb_murder = ReplyKeyboardMarkup(resize_keyboard=True)
kb_murder.add(murder_button)