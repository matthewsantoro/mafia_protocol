from aiogram import Dispatcher, types

from answer_text import Answer
from core.keyboards import kb_client      


async def command_start_help(message: types.Message):
    await message.answer(Answer.HELP.value, reply_markup=kb_client)


# async def _add_data_in_context(state=FsSMContext, key , object):
#     async with state.proxy() as data:
#         pass

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start_help, commands=['start', 'help'])
