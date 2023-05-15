from aiogram.fsm.state import StatesGroup, State


class EditAplicationState(StatesGroup):
    wait_edit_name = State()
    wait_edit_description = State()
    wait_new_language = State()
    wait_edit_language = State()
