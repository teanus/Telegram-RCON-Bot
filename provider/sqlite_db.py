#
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#
#
#
# ████████╗███████╗ █████╗ ███╗   ██╗██╗   ██╗███████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║██╔════╝
#    ██║   █████╗  ███████║██╔██╗ ██║██║   ██║███████╗
#    ██║   ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║╚════██║
#    ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝███████║
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝


from resources import config
import sqlite3 as sql

db = None
cur = None


def sql_start():
    global db, cur
    db = sql.connect(config.database()['name'])
    cur = db.cursor()
    if db:
        print('Sqlite3: connected')
    table_users = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, telegram_id TEXT, role TEXT DEFAULT ' \
                  '"normal") '
    table_black_list = 'CREATE TABLE IF NOT EXISTS black_list(command TEXT)'
    cur.execute(table_users)
    cur.execute(table_black_list)
    db.commit()


def user_add(user_id):
    sql_start()
    query = 'INSERT INTO users(telegram_id, role) VALUES(?, ?)'
    cur.execute(query, [user_id, 'normal', ])
    db.commit()
    return 'Пользователь был добавлен в список'


def admin_add(user_id):
    sql_start()
    query = 'INSERT INTO users(telegram_id, role) VALUES(?, ?)'
    cur.execute(query, [user_id, 'admin', ])
    db.commit()
    return 'Админ был добавлен в список'


def user_remove(user_id):
    sql_start()
    query = 'DELETE FROM users WHERE telegram_id = ?'
    cur.execute(query, (user_id,))
    db.commit()
    return 'Пользователь был успешно удален из бд'


def admin_remove(user_id):
    sql_start()
    query = 'DELETE FROM users WHERE telegram_id= ?'
    cur.execute(query, (user_id,))
    db.commit()
    return 'Администратор успешно удален из бд!'


def add_black_list(cmd):
    sql_start()
    query = "INSERT INTO black_list(command) VALUES(?)"
    cur.execute(query, (cmd,))
    db.commit()
    return 'Команда была заблокирована'


def remove_black_list(cmd):
    sql_start()
    query = f"DELETE FROM black_list WHERE command = ?"
    cur.execute(query, (cmd,))
    db.commit()
    return 'Команда была разблокирована'


def commands_all():
    sql_start()
    query = 'SElECT * FROM black_list'
    result = cur.execute(query).fetchall()
    text = str(result)[1:-1]
    symbols = ['(', ')', ',', '\'']
    for char in symbols:
        text = text.replace(char, '').replace(' ', '\n')
    return text


def command_exists(cmd):
    sql_start()
    query = 'SELECT * FROM black_list WHERE command = ?'
    result = cur.execute(query, (cmd,)).fetchall()
    return bool(len(result))


def user_exists(user_id):
    sql_start()
    query = 'SELECT * FROM users WHERE telegram_id = ?'
    result = cur.execute(query, (user_id,)).fetchall()
    return bool(len(result))


def check_admin_user(user_id):
    sql_start()
    query = f'SELECT role FROM users WHERE telegram_id = ? AND role == ?'
    result = cur.execute(query, (user_id, 'admin')).fetchall()
    return bool(len(result))
