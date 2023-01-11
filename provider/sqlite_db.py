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


class DataBase:
    def __init__(self):
        self.con = sql.connect(config.database()['name'])
        self.cur = self.con.cursor()
        if self.con:
            print('Sqlite3: connected')
        table_users = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, telegram_id TEXT, role TEXT DEFAULT ' \
                      '"normal") '
        table_black_list = 'CREATE TABLE IF NOT EXISTS black_list(command TEXT)'
        self.cur.execute(table_users)
        self.cur.execute(table_black_list)
        self.con.commit()

    def add_user(self, user_id):
        query = 'INSERT INTO users(telegram_id, role) VALUES(?, ?)'
        self.cur.execute(query, [user_id, 'normal', ])
        self.con.commit()
        return 'Пользователь был добавлен в список'

    def user_exists(self, user_id):
        query = 'SELECT * FROM users WHERE telegram_id = ?'
        result = self.cur.execute(query, (user_id,)).fetchall()
        return bool(len(result))

    def user_remove(self, user_id):
        query = 'DELETE FROM users WHERE telegram_id = ?'
        self.cur.execute(query, (user_id,))
        self.con.commit()
        return 'Пользователь был успешно удален из бд'

    def admin_add(self, user_id):
        query = 'INSERT INTO users(telegram_id, role) VALUES(?, ?)'
        self.cur.execute(query, [user_id, 'admin', ])
        self.con.commit()
        return 'Админ был добавлен в список', True

    def check_admin_user(self, user_id):
        query = 'SELECT role FROM users WHERE telegram_id = ? AND role == ?'
        result = self.cur.execute(query, (user_id, 'admin')).fetchall()
        return bool(len(result))

    def admin_remove(self, user_id):
        query = 'DELETE FROM users WHERE telegram_id= ?'
        self.cur.execute(query, (user_id,))
        self.con.commit()
        return 'Администратор успешно удален из бд!'

    def add_black_list(self, cmd):
        query = 'INSERT INTO black_list(command) VALUES(?)'
        self.cur.execute(query, (cmd,))
        self.con.commit()
        return 'Команда была заблокирована'

    def command_exists(self, cmd):
        query = 'SELECT * FROM black_list WHERE command = ?'
        result = self.cur.execute(query, (cmd,)).fetchall()
        return bool(len(result))

    def remove_black_list(self, cmd):
        query = 'DELETE FROM black_list WHERE command = ?'
        self.cur.execute(query, (cmd,))
        self.con.commit()
        return 'Команда была разблокирована'

    def commands_all(self):
        query = 'SElECT * FROM black_list'
        result = self.cur.execute(query).fetchall()
        text = str(result)[1:-1]
        symbols = ['(', ')', ',', '\'']
        for char in symbols:
            text = text.replace(char, '').replace(' ', '\n')
        return text
