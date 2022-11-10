from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from answer_text import Emojis

vote_button = KeyboardButton('Никто не покинул')
kb_vote = ReplyKeyboardMarkup(resize_keyboard=True)
kb_vote.add(vote_button)

murder_button = KeyboardButton('Промах')
kb_murder = ReplyKeyboardMarkup(resize_keyboard=True)
kb_murder.add(murder_button)

skip_button = KeyboardButton('Пропустить')
kb_skip = ReplyKeyboardMarkup(resize_keyboard=True)
kb_skip.add(skip_button)

kb_extra_points = ReplyKeyboardMarkup(resize_keyboard=True)
x = [
    KeyboardButton(Emojis['1']),
    KeyboardButton(Emojis['2']),
    KeyboardButton(Emojis['3']),
    KeyboardButton(Emojis['4']),
    KeyboardButton(Emojis['5']),
    KeyboardButton(Emojis['6']),
    KeyboardButton(Emojis['7']),
    KeyboardButton(Emojis['8']),
    KeyboardButton(Emojis['9']),
    KeyboardButton(Emojis['10']),
    KeyboardButton(Emojis['ok'])
]
kb_extra_points.add(*x)

# 
# kb_extra_points = InlineKeyboardMarkup(row_width=5)
# x = [InlineKeyboardButton(text='1️⃣', callback_data="ep_1"),
#      InlineKeyboardButton(text='2️⃣', callback_data="ep_2"),
#      InlineKeyboardButton(text='3️⃣', callback_data="ep_3"),
#      InlineKeyboardButton(text='4️⃣', callback_data="ep_4"),
#      InlineKeyboardButton(text='5️⃣', callback_data="ep_5"),
#      InlineKeyboardButton(text='6️⃣', callback_data="ep_6"),
#      InlineKeyboardButton(text='7️⃣', callback_data="ep_7"),
#      InlineKeyboardButton(text='8️⃣', callback_data="ep_8"),
#      InlineKeyboardButton(text='9️⃣', callback_data="ep_9"),
#      InlineKeyboardButton(text='🔟', callback_data="ep_10"),
#      InlineKeyboardButton(text='🆗', callback_data="ep_ok"),
#      ]
# kb_extra_points.add(*x)
