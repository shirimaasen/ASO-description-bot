from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message
from aiohttp import ClientSession

from bot.cbdata import MenuCallbackFactory, SelectApplicationCallbackFactory, EditApplicationCallbackFactory, \
    ChooseWhatEditApplicationCallbackFactory, NewLanguageApplicationCallbackFactory, \
    StartCreateApplicationCallbackFactory
from bot.handlers.create_application import start_create_application
from bot.keyboards.default.menu import make_menu_keyboard
from bot.keyboards.inline.application import make_applications_keyboard, make_application_languages_keyboard, \
    make_edit_applications_keyboard, make_what_edit_applications_keyboard
from bot.states.edit_application import EditAplicationState
from bot.utils import application_text, pars_keywords, pars_variable

router = Router()


@router.callback_query(MenuCallbackFactory.filter())
async def main_menu(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("MAIN_MENU_TEXT", reply_markup=make_menu_keyboard())


@router.message(F.text == "Сгенерировать описание")
async def start_generate(message: Message,
                         session: ClientSession):
    applications_responce = await session.get("/application", params={"user_id": message.from_user.id})
    applications = await applications_responce.json()
    await message.answer("Выберите приложение", reply_markup=make_applications_keyboard(applications))


@router.callback_query(SelectApplicationCallbackFactory.filter())
async def select_language(call: CallbackQuery,
                          callback_data: SelectApplicationCallbackFactory,
                          session: ClientSession):
    application_responce = await session.get(f"/application/{callback_data.application_id}")
    application = await application_responce.json()
    await call.message.edit_text(
        f"{application_text(**application)}\nВыбирете язык", reply_markup=make_application_languages_keyboard(
            application_id=application["id"], variables=application["variables"]
        )
    )


@router.message(F.text == "Редактировать приложения")
async def edit_applications(message: Message,
                            session: ClientSession):
    applications_responce = await session.get("/application", params={"user_id": message.from_user.id})
    applications = await applications_responce.json()
    await message.answer("Выберите приложение", reply_markup=make_edit_applications_keyboard(applications))


@router.callback_query(EditApplicationCallbackFactory.filter())
async def choose_what_edit(call: CallbackQuery,
                           callback_data: EditApplicationCallbackFactory,
                           session: ClientSession,
                           bot: Bot):
    await _answes_edit_applocation(
        application_id=callback_data.application_id,
        session=session,
        message_id=call.message.message_id,
        bot=bot,
        chat_id=call.from_user.id
    )


@router.callback_query(ChooseWhatEditApplicationCallbackFactory.filter(F.edit == "name"))
async def choose_dit_name(call: CallbackQuery,
                          callback_data: ChooseWhatEditApplicationCallbackFactory,
                          state: FSMContext):
    new_message = await call.message.answer("Введите новое имя")
    await state.update_data(dict(
        application_id=callback_data.application_id,
        message_id=call.message.message_id,
        delete_message_id=new_message.message_id
    ))
    await state.set_state(EditAplicationState.wait_edit_name)


@router.callback_query(ChooseWhatEditApplicationCallbackFactory.filter(F.edit == "description"))
async def choose_edit_description(call: CallbackQuery,
                                  callback_data: ChooseWhatEditApplicationCallbackFactory,
                                  state: FSMContext):
    new_message = await call.message.answer("Введите новое описание")
    await state.update_data(dict(
        application_id=callback_data.application_id,
        message_id=call.message.message_id,
        delete_message_id=new_message.message_id
    ))
    await state.set_state(EditAplicationState.wait_edit_description)


@router.callback_query(ChooseWhatEditApplicationCallbackFactory.filter())
async def choose_edit_language(call: CallbackQuery,
                               callback_data: ChooseWhatEditApplicationCallbackFactory,
                               state: FSMContext):
    await state.set_state(EditAplicationState.wait_edit_language)
    new_message = await call.message.answer("Введите новые ключевые слова")
    await state.update_data(dict(
        application_id=callback_data.application_id,
        language=callback_data.edit,
        message_id=call.message.message_id,
        delete_message_id=new_message.message_id
    ))


@router.callback_query(NewLanguageApplicationCallbackFactory.filter())
async def choose_new_language(call: CallbackQuery,
                              callback_data: NewLanguageApplicationCallbackFactory,
                              state: FSMContext):
    new_message = await call.message.answer("Укажите язык и ключевые слова \nНапример:\n"
                                            "<code>english: interesting, strategy, replayable</code>")
    await state.update_data(dict(
        application_id=callback_data.application_id,
        message_id=call.message.message_id,
        delete_message_id=new_message.message_id
    ))
    await state.set_state(EditAplicationState.wait_new_language)


@router.message(EditAplicationState.wait_edit_name)
async def edit_name(message: Message,
                    session: ClientSession,
                    state: FSMContext,
                    bot: Bot):
    application_update_data = await state.get_data()
    await _edit_field(
        field="name",
        state_data=application_update_data,
        session=session,
        message=message,
        bot=bot
    )
    await state.clear()


@router.message(EditAplicationState.wait_edit_description)
async def edit_description(message: Message,
                           session: ClientSession,
                           state: FSMContext,
                           bot: Bot):
    application_update_data = await state.get_data()
    await _edit_field(
        field="description",
        state_data=application_update_data,
        session=session,
        message=message,
        bot=bot
    )
    await state.clear()


@router.message(EditAplicationState.wait_edit_language)
async def edit_language(message: Message,
                        session: ClientSession,
                        state: FSMContext,
                        bot: Bot):
    application_update_data = await state.get_data()
    await _edit_language(
        state_data=application_update_data,
        session=session,
        message=message,
        bot=bot,
        is_new=False
    )
    await state.clear()


@router.message(EditAplicationState.wait_new_language)
async def new_language(message: Message,
                       session: ClientSession,
                       state: FSMContext,
                       bot: Bot):
    application_update_data = await state.get_data()
    await _edit_language(
        state_data=application_update_data,
        session=session,
        message=message,
        bot=bot,
        is_new=True
    )
    await state.clear()


@router.callback_query(StartCreateApplicationCallbackFactory.filter())
async def new_application(call: CallbackQuery,
                          session: ClientSession,
                          state: FSMContext):
    await session.post("/user", json={"id": call.from_user.id})
    await start_create_application(call.message, state)


async def _answes_edit_applocation(
        *,
        application_id: str,
        session: ClientSession,
        message_id: int, bot: Bot,
        chat_id: int | str) -> None:
    application_responce = await session.get(f"/application/{application_id}")
    application = await application_responce.json()
    await bot.edit_message_text(
        f"{application_text(**application)}\n\nРедактировать:",
        reply_markup=make_what_edit_applications_keyboard(
            application_id=application["id"], variables=application["variables"]
        ),
        chat_id=chat_id,
        message_id=message_id
    )


async def _edit_language(*,
                         state_data: dict,
                         session: ClientSession,
                         message: Message,
                         bot: Bot,
                         is_new: bool):
    application_responce = await session.get(f"/application/{state_data['application_id']}")
    application = await application_responce.json()
    if is_new:
        new_variable = pars_variable(message.text)
    else:
        new_variable = {
            "language": state_data['language'],
            "keywords": pars_keywords(message.text)
        }
    if variables := application.get('variables'):
        if is_new:
            variables.append(new_variable)
        else:
            variables = [variable for variable in variables if variable["language"] != new_variable["language"]]
            variables.append(new_variable)
    else:
        variables = [new_variable]
    await session.put("/application", json={
        "id": application["id"],
        "variables": variables
    })
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=state_data["delete_message_id"]
    )
    await message.delete()
    await _answes_edit_applocation(
        application_id=state_data['application_id'],
        session=session,
        message_id=state_data["message_id"],
        bot=bot,
        chat_id=message.from_user.id
    )


async def _edit_field(*,
                      field: str,
                      state_data: dict,
                      session: ClientSession,
                      message: Message,
                      bot: Bot, ):
    application_responce = await session.get(f"/application/{state_data['application_id']}")
    application = await application_responce.json()
    await session.put("/application", json={
        "id": application["id"],
        field: message.text
    })
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=state_data["delete_message_id"]
    )
    await message.delete()
    await _answes_edit_applocation(
        application_id=state_data['application_id'],
        session=session,
        message_id=state_data["message_id"],
        bot=bot,
        chat_id=message.from_user.id
    )
