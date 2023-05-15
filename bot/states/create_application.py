from aiogram.fsm.state import StatesGroup, State


class CreateAplicationState(StatesGroup):
    wait_name = State()
    wait_description = State()
    wait_cbdata = State()
    wait_variable = State()
