#Обработка регистрации
from aiogram import types, Dispatcher
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data import message_dict
import asyncio
from keyboards.main_keyboards import *
from data.db_scripts import find_user, add_user
from config import chanel1, chanel2

class FSMmain(StatesGroup):
    start_state = State()
    iwasonmeeting = State()
    get_mes = State()
    get_but = State()
    get_mes_but = State()
    get_url_but = State()
    get_date = State()
    get_time = State()

async def get_user_id(state: FSMContext):
    async with state.proxy() as data:
        return data['user_id']

async def command_start(message : types.Message, state : FSMContext):
    await FSMmain.start_state.set()
    async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['first_name'] = message.from_user.first_name
    if len(await find_user(message.from_user.id)) == 0:
        await add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, message_dict['start_message1'].format(name = message.from_user.first_name), reply_markup = keyboard_start1, parse_mode="Markdown")
    photo = types.InputFile("data\photos\start_photo.jpg")
    await asyncio.sleep(3) 
    await bot.send_photo(message.from_user.id, photo=photo)
    await bot.send_message(message.from_user.id, message_dict['start_message2'], reply_markup = keyboard_start2, parse_mode="Markdown")

async def I_was_on_meeting(callback: types.CallbackQuery):
    await callback.message.answer(message_dict['iwasonmeeting'], reply_markup = keyboard_iwasonmeeting, parse_mode="Markdown")
    await FSMmain.iwasonmeeting.set()
    await callback.answer()

async def offer_for_sub(message : types.Message, state : FSMContext):
    await FSMmain.start_state.set()
    await bot.send_message(message.from_user.id, message_dict['offer1'], parse_mode="Markdown")
    await asyncio.sleep(3)
    await bot.send_message(message.from_user.id, message_dict['offer2'], parse_mode="Markdown")
    await asyncio.sleep(3) 
    await bot.send_message(message.from_user.id, message_dict['offer3'], parse_mode="Markdown")
    await asyncio.sleep(3) 
    await bot.send_message(message.from_user.id, message_dict['offer4'], reply_markup = keyboard_ready, parse_mode="html") 

async def I_am_waiting_for_record(callback: types.CallbackQuery):
    await callback.message.answer(message_dict['record_ready'], reply_markup = keyboard_iamwaitingrecord, parse_mode="Markdown")
    await callback.answer()

async def yay(callback: types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        id = data['user_id']
        first_name = data['first_name']
    await bot.send_message(id, message_dict['yay1'])
    await asyncio.sleep(3)
    await bot.send_message(id, message_dict['yay2'])
    await asyncio.sleep(3)
    await bot.send_message(id, message_dict['yay3'], reply_markup = keyboard_ready, parse_mode="html")
    await callback.answer()

async def check_ready(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id = data['user_id']
        first_name = data['first_name']
    user_channel1_status = await bot.get_chat_member(chat_id=chanel1, user_id=id)
    user_channel2_status = await bot.get_chat_member(chat_id=chanel2, user_id=id)
    status = user_channel1_status['status'] != types.ChatMemberStatus.LEFT and user_channel2_status['status'] != types.ChatMemberStatus.LEFT
    if status:
        await bot.send_message(id, message_dict['get_sub1'].format(name = first_name), reply_markup = keyboard_get_sub1, parse_mode="Markdown")
        await asyncio.sleep(3)
        await bot.send_message(id, message_dict['get_sub2'], parse_mode="Markdown")
        await asyncio.sleep(3) 
        await bot.send_message(id, message_dict['get_sub3'], reply_markup = keyboard_get_sub3, parse_mode="Markdown")
        await asyncio.sleep(3) 
        await bot.send_message(id, message_dict['get_sub4'].format(name = first_name), reply_markup = keyboard_get_sub4, parse_mode="Markdown") 
        await asyncio.sleep(3) 
        await bot.send_message(id, message_dict['get_sub5'].format(name = first_name), parse_mode="Markdown") 
    else:
        await bot.send_message(id, message_dict['no_sub'])
        await bot.send_message(id, message_dict['offer4'], reply_markup = keyboard_ready, parse_mode="html") 
    await callback.answer()    


def register_handlers_registration(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start'], state = '*')
    dp.register_message_handler(offer_for_sub, lambda message: message.text == 'Это точно! Надо чаще встречаться!' or \
                                               message.text == 'И в запись посмотреть тоже неплохо!', state = FSMmain.iwasonmeeting)
    dp.register_callback_query_handler(I_was_on_meeting, Text('iwasonmeeting'),state = FSMmain.start_state)
    dp.register_callback_query_handler(I_am_waiting_for_record, Text('iamwaitingforrecord'),state = FSMmain.start_state)
    dp.register_callback_query_handler(yay, Text('yay'),state = FSMmain.start_state)
    dp.register_callback_query_handler(check_ready, Text('check_ready'),state = FSMmain.start_state)
    
    
