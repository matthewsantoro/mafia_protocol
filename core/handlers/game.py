from collections import namedtuple

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from core.states import FSMGame

from answer_text import Answer, Emojis
from core.keyboards import kb_extra_points, kb_murder, kb_skip, kb_vote
from typing import List

import re
from  core.handlers.check_game_valid_data import *




    
async def start_getting_extra_points(message: types.Message):
    await message.answer(Answer.EXTRA_POINT.value, reply_markup=kb_extra_points)
    await FSMGame.extra_point.set()


async def get_extra_points(message: types.Message, state=FSMContext):
    print(message.text)
    print(message.text in Emojis.values())
    if message.text == Emojis['ok']:
        await get_result_game(message, state)
        await state.finish()
    else:
        async with state.proxy() as data:
            if not data.get('extra_points'):
                data['extra_points'] = {}
            if message.text in Emojis.values():
                await message.answer(Answer.EXTRA_POINT_VALUE.value)
                data['active_extra_point_player'] = list(
                    Emojis.keys())[list(Emojis.values()).index(message.text)]
            else:
                extra_point = float(message.text.replace(',', '.'))
                playres_number = data['active_extra_point_player']
                data['extra_points'][playres_number] = extra_point
                await message.answer(Answer.EXTRA_POINT.value, reply_markup=kb_extra_points)


async def get_result_game(message: types.Message, state=FSMContext):
    answer = ''
    async with state.proxy() as data:
        print(data)
        for i, nick in enumerate(data['nicks']):
            answer += f'{i+1}. {nick}\n'
        answer += f"\nЧерная команда: {data['roles'].don }-{data['roles'].maf_1}-{data['roles'].maf_2}\n"
        answer += f"Дон: {data['roles'].don}\n"
        answer += f"Шериф: {data['roles'].sheriff}\n"
        for i, day in enumerate(data['days']):
            answer += f"{i}) Голосование: {day['nomination']} (Выгнали: {day['vote']})\n"
        answer += f"\nОтстрелили: "
        for i, night in enumerate(data['nights']):
            answer += f"{night['murder']} "
        answer += '\nПроверки дона:'
        for i, night in enumerate(data['nights']):
            x = night['don_check']
            answer += f"{ x if x is not None else ''} "
        answer += '\nПроверки шерифа:'
        for i, night in enumerate(data['nights']):
            x = night['sheriff_check']
            answer += f" { x if x is not None else ''}"
        answer += f"\nЛХ: {data['best_move']}"
        answer += f"\nДопы\n:"
        for key in data['extra_points']:
            answer += f"{data['nicks'][int(key)-1]} : {data['extra_points'][key]}"
        await message.answer(answer)

async def new_game(message: types.Message):
    await FSMGame.nicks.set()
    await message.answer(Answer.NICK.value)


async def get_nick(message: types.Message, state=FSMContext):
    nicks = message.text.split()
    if check_valid_nick(nicks):
        async with state.proxy() as data:
            data['nicks'] = nicks
            data['active_players'] = list(range(1,11))
        await FSMGame.roles.set()
        await message.answer(Answer.ROLE.value)
    else:
        await message.answer(Answer.NICK_ERROR.value)



async def get_roles(message: types.Message, state=FSMContext):
    Roles = namedtuple('Roles', 'don maf_1 maf_2 sheriff')
    if check_valid_roles(message.text):    
        roles = Roles(*[int(x) for x in message.text.split()])
        async with state.proxy() as data:
            data["roles"] = roles
        await message.answer(Answer.NOMINATIONS.value, reply_markup=kb_skip)
        await FSMGame.nomination.set()
    else:
        await message.answer(Answer.COMMON_ERROR.value)
    


async def get_nominations(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if not data.get('days'):
                    data['days'] = []
                    
        if message.text == kb_vote.keyboard[0][0].text:
            nominations = 'Без голосования'
            await message.answer(Answer.VOTE.value, reply_markup=kb_skip)
            await FSMGame.votes.set()
            
        elif check_valid_nominations(message.text , data['active_players']):     
            nominations = str_to_digit_list_int(message.text)       
            data['days'].append({'nomination': nominations})
            await message.answer(Answer.VOTE.value, reply_markup=kb_skip)
            await FSMGame.votes.set()
            
        else: await message.answer(Answer.COMMON_ERROR.value, reply_markup=kb_skip)
    




async def get_vote(message: types.Message, state=FSMContext):        
    if message.text == kb_skip.keyboard[0][0].text:
        vote = '-'
    else:
        vote = message.text
    async with state.proxy() as data:
        data['days'][-1]['vote'] = vote
    await message.answer(Answer.MURDER.value, reply_markup=kb_skip)
    await FSMGame.murder.set()


async def get_murder(message: types.Message, state=FSMContext):
    if message.text == kb_murder.keyboard[0][0].text:
        murder = None
    else:
        murder = int(message.text)
    async with state.proxy() as data:
        if not data.get('nights'):
            data['nights'] = []
        data['nights'].append({'murder': murder})
    await message.answer(Answer.DON_CHECK.value, reply_markup=kb_skip)
    await FSMGame.don_check.set()


async def get_don_check(message: types.Message, state=FSMContext):
    if message.text == kb_skip.keyboard[0][0].text:
        check = None
    else:
        check = int(message.text)
    async with state.proxy() as data:
        data['nights'][-1]['don_check'] = check
    await message.answer(Answer.SHERIFF_CHECK.value, reply_markup=kb_skip)
    await FSMGame.sheriff_check.set()


async def get_sheriff_check(message: types.Message, state=FSMContext):
    if message.text == kb_skip.keyboard[0][0].text:
        check = None
    else:
        check = int(message.text)
    async with state.proxy() as data:
        data['nights'][-1]['sheriff_check'] = check
        if not data.get('best_move'):
            await message.answer(Answer.BEST_MOVE.value)
            await FSMGame.best_move.set()
        else:
            await message.answer(Answer.NOMINATIONS.value)
            await FSMGame.nomination.set()


async def get_best_move(message: types.Message, state=FSMContext):
    if message.text == kb_skip.keyboard[0][0].text:
        best_move = None
    else:
        best_move = message.text
    async with state.proxy() as data:
        data['best_move'] = best_move
    await message.answer(Answer.NOMINATIONS.value)
    await FSMGame.nomination.set()
    
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        get_extra_points, state=FSMGame.extra_point)
    dp.register_message_handler(
        start_getting_extra_points, state='*', commands=['Закончить'])
    dp.register_message_handler(new_game, commands=['new_game'], state=None)
    dp.register_message_handler(get_nick, state=FSMGame.nicks)
    dp.register_message_handler(get_roles, state=FSMGame.roles)
    dp.register_message_handler(get_nominations, state=FSMGame.nomination)
    dp.register_message_handler(get_vote, state=FSMGame.votes)
    dp.register_message_handler(get_murder, state=FSMGame.murder)
    dp.register_message_handler(get_don_check, state=FSMGame.don_check)
    dp.register_message_handler(get_sheriff_check, state=FSMGame.sheriff_check)
    dp.register_message_handler(get_best_move, state=FSMGame.best_move)