from aiogram import types, Dispatcher, Bot
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from handlers.main_handler import FSMmain
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import RetryAfter
from data import message_dict
from config import admin
from keyboards.mailing_keyboards import kb_add_button
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from data.db_scripts import get_users, add_mailing, get_mailing
import asyncio

async def make_mailing(message : types.Message, state : FSMContext):
    if message.from_user.id == admin:
        await bot.send_message(message.from_user.id, "Введите сообщение для рассылки:")
        await FSMmain.get_mes.set()

async def get_mes(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['id_mes'] = message.message_id
    await bot.send_message(message.from_user.id, "Супер! Будем добавлять кнопку со ссылкой?", reply_markup = kb_add_button)
    await FSMmain.get_but.set()

async def add_button(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['flag'] = 1
    await bot.send_message(message.from_user.id, "Введите текст кнопки:")
    await FSMmain.get_mes_but.set()

async def get_mes_but(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['but_text'] = message.text
    await bot.send_message(message.from_user.id, "Введите ссылку кнопки:")
    await FSMmain.get_url_but.set()

async def get_url_but(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['but_url'] = message.text
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(text = data['but_text'], url = data['but_url']))
        await confirm_mes(message, bot, data['id_mes'], kb)

async def confirm_mes(message:types.Message, bot:Bot, message_id: int, reply_kb : InlineKeyboardMarkup = None):
    await message.answer('Вот такое сообщение будет отправлено:')
    await bot.copy_message(admin, admin, message_id, reply_markup = reply_kb)
    await message.answer('Чтобы изменить сообщение введите снова /mailing \nВведите дату отправки в формате dd:mm:yy')
    await FSMmain.get_date.set()

async def get_date(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await bot.send_message(message.from_user.id, "Введите время отпрвки HH:MM:")
    await FSMmain.get_time.set()

async def get_time(message : types.Message, state : FSMContext, scheduler: AsyncIOScheduler):
    async with state.proxy() as data:
        data['time'] = message.text
        time = data['time'].split(':')
        date = f"{data['date']}.{time[0]}.{time[1]}"
        send_date = datetime.datetime.strptime(date, "%d.%m.%y.%H.%M")
        await add_mailing(date, data['id_mes'], data['flag'], data['but_text'], data['but_url'])
        scheduler.add_job(send_mailing, trigger = 'date', run_date =  send_date, kwargs = {'state' : state, 'mailing_id' : date})  
    await bot.send_message(message.from_user.id, "Успешно запланировано!")
    await FSMmain.start_state.set()

async def conf(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['flag'] = 0
        data['but_text'] = ''
        data['but_url'] = ''
        await confirm_mes(message, bot, data['id_mes'])

async def send_mes(bot, user_id, admin, id, kb):
    await bot.copy_message(user_id, admin, id, reply_markup = kb)

async def send_mailing(state: FSMContext, mailing_id:str):
    data = await get_mailing(mailing_id)  
    data = data[0]
    kb = InlineKeyboardMarkup()
    if int(data[1]) == 1:
        kb.add(InlineKeyboardButton(text = data[2], url = data[3]))
    id = data[0]
    for user in get_users():
        await asyncio.sleep(.05)
        user_id = user[0]
        try:
            await send_mes(bot, user_id, admin, id, kb)
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await send_mes(bot, user_id, admin, id, kb)


def register_handlers_registration(dp : Dispatcher):
    dp.register_message_handler(make_mailing, commands = ['mailing'], state = '*')
    dp.register_message_handler(get_mes, state = FSMmain.get_mes, content_types=types.ContentTypes.ANY)
    dp.register_message_handler(get_mes_but, state = FSMmain.get_mes_but)
    dp.register_message_handler(get_url_but, state = FSMmain.get_url_but)
    dp.register_message_handler(get_date, state = FSMmain.get_date)
    dp.register_message_handler(get_time, state = FSMmain.get_time, )
    dp.register_message_handler(add_button, lambda message: message.text == 'Да, добавить кнопку', state = FSMmain.get_but)
    dp.register_message_handler(conf, lambda message: message.text == 'Нет, продолжить', state = FSMmain.get_but)