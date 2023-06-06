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


from os import getenv

import aiosqlite
import asyncpg
from dotenv import load_dotenv

from resources import config

load_dotenv()


class SqliteDatabase:
    def __init__(self):
        self.con = None
        self.cur = None

    async def connect(self):
        try:
            self.con = await aiosqlite.connect(config.sqlite()["name"])
            self.cur = await self.con.cursor()
            if self.con:
                print("SQLite: подключился")
            table_users = (
                "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, telegram_id TEXT, role TEXT "
                "DEFAULT "
                "'normal') "
            )
            table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
            await self.execute_query(table_users)
            await self.execute_query(table_black_list)
            await self.con.commit()
        except aiosqlite.Error as e:
            print(f"Ошибка при подключении к базе данных SQLite: {e}")

    async def disconnect(self):
        if self.con:
            await self.con.close()

    async def execute_query(self, query, params=None):
        try:
            if not self.con:
                await self.connect()
            if params:
                async with self.con.execute(query, params):
                    pass
            else:
                async with self.con.execute(query):
                    pass
            await self.con.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка при выполнении запроса SQLite: {e}")
            return False

    async def fetch_all(self, query, params=None):
        try:
            if not self.con:
                await self.connect()
            if params:
                async with self.con.execute(query, params) as cur:
                    result = await cur.fetchall()
            else:
                async with self.con.execute(query) as cur:
                    result = await cur.fetchall()
            return result
        except aiosqlite.Error as e:
            print(f"Ошибка при выполнении запроса SQLite: {e}")
            return []

    async def add_user(self, user_id):
        query = "INSERT INTO users(telegram_id, role) VALUES(?, ?)"
        return await self.execute_query(query, [user_id, "normal"])

    async def user_exists(self, user_id):
        query = "SELECT * FROM users WHERE telegram_id = ?"
        result = await self.fetch_all(query, (user_id,))
        return bool(len(result))

    async def user_remove(self, user_id):
        query = "DELETE FROM users WHERE telegram_id = ?"
        return await self.execute_query(query, (user_id,))

    async def admin_add(self, user_id):
        query = "INSERT INTO users(telegram_id, role) VALUES(?, ?)"
        return await self.execute_query(query, [user_id, "admin"])

    async def check_admin_user(self, user_id):
        query = "SELECT role FROM users WHERE telegram_id = ? AND role = ?"
        result = await self.fetch_all(query, (user_id, "admin"))
        return bool(len(result))

    async def admin_remove(self, user_id):
        query = "DELETE FROM users WHERE telegram_id = ?"
        return await self.execute_query(query, (user_id,))

    async def add_black_list(self, cmd):
        query = "INSERT INTO black_list(command) VALUES(?)"
        return await self.execute_query(query, (cmd,))

    async def command_exists(self, cmd):
        query = "SELECT * FROM black_list WHERE command = ?"
        result = await self.fetch_all(query, (cmd,))
        return bool(len(result))

    async def remove_black_list(self, cmd):
        query = "DELETE FROM black_list WHERE command = ?"
        return await self.execute_query(query, (cmd,))

    async def commands_all(self):
        query = "SELECT command FROM black_list"
        result = await self.fetch_all(query)
        return "\n".join([row[0] for row in result])


class PostgresqlDatabase:
    def __init__(self):
        self.con = None
        self.cur = None

    async def connect(self):
        try:
            self.con = await asyncpg.connect(
                user=getenv("postgre_username"),
                password=getenv("postgre_password"),
                database=config.postgresql()["name"],
                host=getenv("postgre_host"),
                port=getenv("postgre_port"),
            )
            self.cur = await self.con.cursor()
            if self.con:
                print("PostgreSQL: подключился")
            table_users = (
                "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, telegram_id TEXT, role TEXT "
                "DEFAULT normal "
            )
            table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
            await self.execute_query(table_users)
            await self.execute_query(table_black_list)
            await self.con.commit()
        except asyncpg as e:
            print(f"Ошибка при подключении к базе данных PostgreSQL: {e}")

    async def disconnect(self):
        if self.con:
            await self.con.close()

    async def execute_query(self, query, params=None):
        try:
            if not self.con:
                await self.connect()
            if params:
                await self.cur.execute(query, params)
            else:
                await self.cur.execute(query)
            await self.con.commit()
            return True
        except asyncpg as e:
            print(f"Ошибка при выполнении запроса PostgreSQL: {e}")
            return False

    async def fetch_all(self, query, params=None):
        try:
            if not self.con:
                await self.connect()
            if params:
                await self.cur.execute(query, params)
            else:
                await self.cur.execute(query)
            return await self.cur.fetchall()
        except asyncpg as e:
            print(f"Ошибка при выполнении запроса PostgreSQL: {e}")
            return []

    async def add_user(self, user_id):
        query = "INSERT INTO users(telegram_id, role) VALUES($1, $2)"
        return await self.execute_query(query, [user_id, "normal"])

    async def user_exists(self, user_id):
        query = "SELECT * FROM users WHERE telegram_id = $1"
        result = await self.fetch_all(query, (user_id,))
        return bool(len(result))

    async def user_remove(self, user_id):
        query = "DELETE FROM users WHERE telegram_id = $1"
        return await self.execute_query(query, (user_id,))

    async def admin_add(self, user_id):
        query = "INSERT INTO users(telegram_id, role) VALUES($1, $2)"
        return await self.execute_query(query, [user_id, "admin"])

    async def check_admin_user(self, user_id):
        query = "SELECT role FROM users WHERE telegram_id = $1 AND role = $2"
        result = await self.fetch_all(query, (user_id, "admin"))
        return bool(len(result))

    async def admin_remove(self, user_id):
        query = "DELETE FROM users WHERE telegram_id = $1"
        return await self.execute_query(query, (user_id,))

    async def add_black_list(self, cmd):
        query = "INSERT INTO black_list(command) VALUES($1)"
        return await self.execute_query(query, (cmd,))

    async def command_exists(self, cmd):
        query = "SELECT * FROM black_list WHERE command = $1"
        result = await self.fetch_all(query, (cmd,))
        return bool(len(result))

    async def remove_black_list(self, cmd):
        query = "DELETE FROM black_list WHERE command = $1"
        return await self.execute_query(query, (cmd,))

    async def commands_all(self):
        query = "SELECT command FROM black_list"
        result = await self.fetch_all(query)
        return "\n".join([row[0] for row in result])


class DataBase:
    def __init__(self, db_type):
        self.db_type = db_type.lower()
        if self.db_type == "sqlite":
            self.database = SqliteDatabase()
        elif self.db_type == "postgresql":
            self.database = PostgresqlDatabase()
        else:
            print(
                f"{db_type} - неподдерживаемый тип базы данных.\nИспользуйте PostgreSQL или SQLite"
            )

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

    async def add_user(self, user_id):
        return await self.database.add_user(user_id)

    async def user_exists(self, user_id):
        return await self.database.user_exists(user_id)

    async def user_remove(self, user_id):
        return await self.database.user_remove(user_id)

    async def admin_add(self, user_id):
        return await self.database.admin_add(user_id)

    async def check_admin_user(self, user_id):
        return await self.database.check_admin_user(user_id)

    async def admin_remove(self, user_id):
        return await self.database.admin_remove(user_id)

    async def add_black_list(self, cmd):
        return await self.database.add_black_list(cmd)

    async def command_exists(self, cmd):
        return await self.database.command_exists(cmd)

    async def remove_black_list(self, cmd):
        return await self.database.remove_black_list(cmd)

    async def commands_all(self):
        return await self.database.commands_all()


db = DataBase(db_type=config.database()["type"])
