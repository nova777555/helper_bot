from aiogram.utils import executor
from create_bot import dp
from data.db_scripts import db_load
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from middlewares.scheduler import SchedulerMiddleware

scheduler = AsyncIOScheduler(timezone = "Asia/Irkutsk")
dp.setup_middleware(SchedulerMiddleware(scheduler))
scheduler.start()
#Регистрация всех обработчиков
#Важен порядок handler'ов
from handlers import main_handler
from handlers import mailing
mailing.register_handlers_registration(dp)
main_handler.register_handlers_registration(dp)


#Выполнение при старте бота
async def on_start(_):
    db_load()
    print('Bot is online')
    print(datetime.datetime.now())

#Запуск работы бота
executor.start_polling(dp,skip_updates = True, on_startup = on_start)