from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMGame(StatesGroup):
    nicks = State()
    roles = State()
    nomination = State()
    votes = State()
    murder = State()
    don_check = State()
    sheriff_check = State()
    check_role = State()
    best_move = State()
    extra_point = State()