from aiogram.filters.callback_data import CallbackData


class ApplicationCreateCallbackFactory(CallbackData, prefix="application_create"):
    ...


class ApplicationAddVariableCallbackFactory(CallbackData, prefix="application_add_variable"):
    ...


class GenerateCallbackFactory(CallbackData, prefix="generate"):
    application_id: str
    language: str


class MenuCallbackFactory(CallbackData, prefix="menu"):
    ...


class SelectApplicationCallbackFactory(CallbackData, prefix="select_app"):
    application_id: str


class EditApplicationCallbackFactory(CallbackData, prefix="edit_app"):
    application_id: str


class ChooseWhatEditApplicationCallbackFactory(EditApplicationCallbackFactory, prefix="choose_what_edit_app"):
    edit: str


class NewLanguageApplicationCallbackFactory(EditApplicationCallbackFactory, prefix="choose_what_edit_app"):
    ...


class StartCreateApplicationCallbackFactory(CallbackData, prefix="start_create_application"):
    ...
