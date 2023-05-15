from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiohttp import ClientSession

from bot.cbdata import ApplicationCreateCallbackFactory, ApplicationAddVariableCallbackFactory
from bot.keyboards.inline.application import make_create_application_keyboard
from bot.keyboards.inline.generate import make_generate_keyboard
from bot.states.create_application import CreateAplicationState
from bot.utils import application_text, pars_variable

router = Router()


@router.message(CreateAplicationState.wait_name)
async def set_name(message: Message,
                   state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите краткое описание игры на английском(10-30 слов).")
    await state.set_state(CreateAplicationState.wait_description)


@router.message(CreateAplicationState.wait_description)
async def set_description(message: Message,
                          state: FSMContext):
    await state.update_data(description=message.text)
    application_data = await state.get_data()
    await message.answer(application_text(**application_data), reply_markup=make_create_application_keyboard())
    await state.set_state(CreateAplicationState.wait_cbdata)


@router.callback_query(ApplicationCreateCallbackFactory.filter(), CreateAplicationState.wait_cbdata)
async def create(call: CallbackQuery,
                 session: ClientSession,
                 state: FSMContext):
    application_data = await state.get_data()
    application_data["user_id"] = call.from_user.id
    application_responce = await session.post("/application", json=application_data)
    application = await application_responce.json()
    await call.message.edit_text(
        application_text(**application),
        reply_markup=make_generate_keyboard(
            application_id=application["_id"],
            languages=[variable["language"] for variable in application["variables"]]
        ))
    await state.clear()


@router.message(CreateAplicationState.wait_variable)
async def set_variable(message: Message,
                       state: FSMContext):
    application_data = await state.get_data()
    if variable := pars_variable(message.text):
        if variables := application_data.get('variables'):
            variables.append(variable)
        else:
            variables = [variable]

        await state.update_data(variables=variables)
        application_data = await state.get_data()
        await message.answer(application_text(**application_data), reply_markup=make_create_application_keyboard())
        await state.set_state(CreateAplicationState.wait_cbdata)

    else:
        await message.answer("Нераспознал, попробуй еще раз пример:\n"
                             "<code>english: interesting, strategy, replayable</code>")


@router.callback_query(ApplicationAddVariableCallbackFactory.filter(), CreateAplicationState.wait_cbdata)
async def add_variable(call: CallbackQuery,
                       state: FSMContext):
    await call.message.edit_text("Укажите язык и ключевые слова \nНапример:\n"
                                 "<code>english: interesting, strategy, replayable</code>")
    await state.set_state(CreateAplicationState.wait_variable)


async def start_create_application(message: Message,
                                   state: FSMContext):
    await message.answer("Введите название нового приложения.")
    await state.set_state(CreateAplicationState.wait_name)
