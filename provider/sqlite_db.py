#           Free версия бота проекта LostWeyn
#               Telegram: t.me/lostweyn_project
#  #
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#               24serv: talk.24serv.pro/u/teanus
#  #
#  #
#      ██╗      ██████╗ ███████╗████████╗██╗    ██╗███████╗██╗   ██╗███╗   ██╗
#      ██║     ██╔═══██╗██╔════╝╚══██╔══╝██║    ██║██╔════╝╚██╗ ██╔╝████╗  ██║
#      ██║     ██║   ██║███████╗   ██║   ██║ █╗ ██║█████╗   ╚████╔╝ ██╔██╗ ██║
#      ██║     ██║   ██║╚════██║   ██║   ██║███╗██║██╔══╝    ╚██╔╝  ██║╚██╗██║
#      ███████╗╚██████╔╝███████║   ██║   ╚███╔███╔╝███████╗   ██║   ██║ ╚████║
#      ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝


from Config import db_name
from locales import lang
import sqlite3 as sql


def sql_start():
    global db, cur
    db = sql.connect(db_name)
    cur = db.cursor()
    if db:
        print('Sqlite3: connected')
    query = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, telegram_id TEXT, role TEXT DEFAULT "normal")'
    cur.execute(query)
    db.commit()


def user_add(user_id):
    sql_start()
    query = 'INSERT INTO users(telegram_id, role) VALUES(?, ?)'
    cur.execute(query, [user_id, 'normal'])
    db.commit()
    return lang.message_sqlite_add_normal


def admin_add(user_id):
    sql_start()
    query = 'INSERT INTO users(telegram_id, role) VALUES(?, ?)'
    cur.execute(query, [user_id, 'admin'])
    db.commit()
    return lang.message_sqlite_add_admin


def user_exists(user_id):
    sql_start()
    query = 'SELECT * FROM users WHERE telegram_id = ?'
    result = cur.execute(query, (user_id,)).fetchall()
    db.commit()
    return bool(len(result))


def check_admin_user(user_id):
    sql_start()
    query = f'SELECT role FROM users WHERE telegram_id = ? AND role == ?'
    result = cur.execute(query, (user_id, 'admin')).fetchall()
    db.commit()
    return bool(len(result))
