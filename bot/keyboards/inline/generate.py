from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import GenerateCallbackFactory, MenuCallbackFactory


def make_generate_keyboard(application_id: str, languages: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*(
        InlineKeyboardButton(
            text=language,
            callback_data=GenerateCallbackFactory(
                application_id=application_id,
                language=language
            ).pack()
        ) for language in languages
    ), width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="Главное меню",
            callback_data=MenuCallbackFactory().pack()
        )
    )
    return keyboard.as_markup()
