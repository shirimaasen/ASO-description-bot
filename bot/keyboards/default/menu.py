from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def make_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="Сгенерировать описание"))
    keyboard.add(KeyboardButton(text="Редактировать приложения"))
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
