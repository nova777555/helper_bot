import sqlite3 as sq

#Подключение к БД
def db_load():
    global base, cur
    base = sq.connect('data\db.db')
    cur = base.cursor()
    if base:
        print("Data base has loaded succesfully!")

#Добавление нового пользвателя в БД в таблицу users
async def add_user(id):
    cur.execute(f'INSERT INTO users VALUES (?)', (id,))
    base.commit()

#Добавление новой рассылки
async def add_mailing(mail_id, mes_id, flag, mes_but, url_but):
    cur.execute(f'INSERT INTO mailing VALUES (?, ?, ?, ?, ?)', (mail_id, mes_id, flag, mes_but, url_but))
    base.commit()

async def get_mailing(id):
    print(id)
    cur.execute(f"SELECT mes_id, flag, mes_but, url_but FROM mailing WHERE mailing_id = '{id.strip()}'")
    return list(cur.fetchall())

async def find_user(id):
    cur.execute(f'SELECT id FROM users WHERE id = {id}')
    return list(cur.fetchall())

#Получение всх пользователей бота
def get_users():
    cur.execute('SELECT id FROM users')
    return cur.fetchall()
