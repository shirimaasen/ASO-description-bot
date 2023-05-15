from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from ...cbdata import (
    ApplicationCreateCallbackFactory,
    ApplicationAddVariableCallbackFactory,
    SelectApplicationCallbackFactory,
    GenerateCallbackFactory,
    EditApplicationCallbackFactory,
    ChooseWhatEditApplicationCallbackFactory,
    NewLanguageApplicationCallbackFactory,
    StartCreateApplicationCallbackFactory
)


def make_create_application_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Создать",
            callback_data=ApplicationCreateCallbackFactory().pack()
        ),
        InlineKeyboardButton(
            text="Добавьте ключевые слова",
            callback_data=ApplicationAddVariableCallbackFactory().pack()
        )
    )
    return keyboard.as_markup()


def make_applications_keyboard(applications: list[dict[str, str]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*(
        InlineKeyboardButton(
            text=application["name"],
            callback_data=SelectApplicationCallbackFactory(application_id=application["id"]).pack()
        ) for application in applications
    ), width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="Добавить новое",
            callback_data=StartCreateApplicationCallbackFactory().pack()
        )
    )
    return keyboard.as_markup()


def make_edit_applications_keyboard(applications: list[dict[str, str]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*(
        InlineKeyboardButton(
            text=application["name"],
            callback_data=EditApplicationCallbackFactory(application_id=application["id"]).pack()
        ) for application in applications
    ), width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="Добавить новое",
            callback_data=StartCreateApplicationCallbackFactory().pack()
        )
    )
    return keyboard.as_markup()


def make_what_edit_applications_keyboard(application_id: str, variables: list[dict[str, ...]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Имя",
            callback_data=ChooseWhatEditApplicationCallbackFactory(
                application_id=application_id,
                edit="name").pack()
        ),
        InlineKeyboardButton(
            text="Описание",
            callback_data=ChooseWhatEditApplicationCallbackFactory(
                application_id=application_id,
                edit="description").pack()
        ),
        width=1
    )
    keyboard.row(*(
        InlineKeyboardButton(
            text=variable["language"],
            callback_data=ChooseWhatEditApplicationCallbackFactory(
                application_id=application_id,
                edit=variable["language"]).pack()
        ) for variable in variables
    ), width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="Добавить новый язык",
            callback_data=NewLanguageApplicationCallbackFactory(
                application_id=application_id).pack()
        )
    )
    return keyboard.as_markup()


def make_application_languages_keyboard(application_id: str, variables: list[dict[str, ...]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(*(
        InlineKeyboardButton(
            text=variable["language"],
            callback_data=GenerateCallbackFactory(
                application_id=application_id,
                language=variable["language"]).pack()
        ) for variable in variables
    ), width=2)
    return keyboard.as_markup()
