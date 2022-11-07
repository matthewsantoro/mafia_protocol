from aiogram import types, Dispatcher
from answer_text import Answer
from create_bot import dp 
from keyboards import kb_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from collections import namedtuple


class FSMGame(StatesGroup):
    nicks = State()
    role_selection = State()    
    nomination = State()
    vote = State()
    murder = State()
    check_role = State()
    best_move = State()
    
    
    
async def command_start_help(message : types.Message):
    await message.answer(Answer.HELP.value , reply_markup=kb_client)
  
    
async def new_game(message : types.Message):
    await FSMGame.nicks.set()
    await message.reply(Answer.NICK.value)
  

async def get_nick(message: types.Message, state=FSMContext):
    nicks = message.text.split()
    if len(nicks) == 10: 
        async with state.proxy() as data:
            data['nicks'] = nicks
        await FSMGame.role_selection.set()
        await message.reply(Answer.ROLE.value)
    else: await message.reply(Answer.NICK_ERROR.value)


async def get_roles(message: types.Message, state=FSMContext):
    Roles = namedtuple('Roles', 'don maf_1 maf_2 sherif')
    roles = Roles(*[int(x) for x in message.text.split()])
    async with state.proxy() as data:
        data["roles"] = roles
        print(data)
    await message.reply(Answer.NOMINATIONS.value)
    await FSMGame.nomination.set()
    
async def get_nominations(message: types.Message, state=FSMContext):
    nominations = [int(x) for x in message.text.split()]
    async with state.proxy() as data:
        if data.get('nominations'):
            data['nominations'].append(nominations)
        else: 
            data['nominations'] = []
            data['nominations'].append(nominations)
        print(data['nominations'])
    await message.reply(Answer.vote.value)
    await FSMGame.vote.set()        
    
    
    
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start_help, commands=['start','help'])
    dp.register_message_handler(new_game, commands=['new_game'], state=None)
    dp.register_message_handler(get_nick, state=FSMGame.nicks)
    dp.register_message_handler(get_roles,state=FSMGame.role_selection)
    dp.register_message_handler(get_nominations,state=FSMGame.nomination)
    dp.register_message_handler(get_nominations,state=FSMGame.vote)