from aiogram.fsm.state import StatesGroup, State

class Add(StatesGroup):
    link = State()

class Remove(StatesGroup):
    id = State()