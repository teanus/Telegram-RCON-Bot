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

    async def connect(self) -> None:
        try:
            self.con = await aiosqlite.connect(config.sqlite()["name"])
            print("SQLite подключился")
            await self.initialize_tables()
        except aiosqlite.Error as error:
            print(f"Ошибка при подключении к базе данных SQLite: {error}")

    async def disconnect(self) -> None:
        if self.con:
            await self.con.close()

    async def initialize_tables(self) -> None:
        table_users = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY, 
                telegram_id TEXT, 
                role TEXT DEFAULT 'normal'
            )
        """
        table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
        await self.execute_query(table_users)
        await self.execute_query(table_black_list)
        await self.con.commit()

    async def execute_query(self, query: str, params=None) -> bool:
        try:
            if not self.con:
                await self.connect()
            async with self.con.execute(query, params or ()) as cursor:
                pass
            await self.con.commit()
            return True
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return False

    async def fetch_all(self, query: str, params=None) -> list:
        try:
            if not self.con:
                await self.connect()
            async with self.con.execute(query, params or ()) as cursor:
                result = await cursor.fetchall()
            return result
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return []

    async def add_user(self, user_id: str) -> bool:
        query = "INSERT INTO users(telegram_id, role) VALUES(?, ?)"
        return await self.execute_query(query, [user_id, "normal"])

    async def user_exists(self, user_id: str) -> bool:
        query = "SELECT 1 FROM users WHERE telegram_id = ?"
        result = await self.fetch_all(query, (user_id,))
        return bool(result)

    async def user_remove(self, user_id: str) -> bool:
        query = "DELETE FROM users WHERE telegram_id = ?"
        return await self.execute_query(query, (user_id,))

    async def add_admin(self, user_id: str) -> bool:
        query = "INSERT INTO users(telegram_id, role) VALUES(?, ?)"
        return await self.execute_query(query, [user_id, "admin"])

    async def check_admin_user(self, user_id: str) -> bool:
        query = "SELECT 1 FROM users WHERE telegram_id = ? AND role = ?"
        result = await self.fetch_all(query, (user_id, "admin"))
        return bool(result)

    async def admin_remove(self, user_id: str) -> bool:
        query = "DELETE FROM users WHERE telegram_id = ?"
        return await self.execute_query(query, (user_id,))

    async def add_black_list(self, cmd: str) -> bool:
        query = "INSERT INTO black_list(command) VALUES(?)"
        return await self.execute_query(query, (cmd,))

    async def command_exists(self, cmd: str) -> bool:
        query = "SELECT 1 FROM black_list WHERE command = ?"
        result = await self.fetch_all(query, (cmd,))
        return bool(result)

    async def remove_black_list(self, cmd: str) -> bool:
        query = "DELETE FROM black_list WHERE command = ?"
        return await self.execute_query(query, (cmd,))

    async def commands_all(self) -> str:
        query = "SELECT command FROM black_list"
        result = await self.fetch_all(query)
        return "\n".join([row[0] for row in result])


class PostgresqlDatabase:
    def __init__(self):
        self.con = None

    async def connect(self) -> None:
        try:
            self.con = await asyncpg.connect(
                user=getenv("postgre_username"),
                password=getenv("postgre_password"),
                database=config.postgresql()["name"],
                host=getenv("postgre_host"),
                port=getenv("postgre_port"),
            )
            print("PostgreSQL: подключился")
            await self.initialize_tables()
        except asyncpg.PostgresError as error:
            print(f"Ошибка при подключении к базе данных PostgreSQL: {error}")

    async def disconnect(self) -> None:
        if self.con:
            await self.con.close()

    async def initialize_tables(self) -> None:
        table_users = """
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY, 
                telegram_id TEXT, 
                role TEXT DEFAULT 'normal'
            )
        """
        table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
        await self.execute_query(table_users)
        await self.execute_query(table_black_list)
        await self.con.commit()

    async def execute_query(self, query: str, params=None) -> bool:
        try:
            if not self.con:
                await self.connect()
            await self.con.execute(query, *params or ())
            await self.con.commit()
            return True
        except asyncpg.PostgresError as error:
            print(f"Ошибка при выполнении запроса PostgreSQL: {error}")
            return False

    async def fetch_all(self, query: str, params=None) -> list:
        try:
            if not self.con:
                await self.connect()
            result = await self.con.fetch(query, *params or ())
            return result
        except asyncpg.PostgresError as error:
            print(f"Ошибка при выполнении запроса PostgreSQL: {error}")
            return []

    async def add_user(self, user_id: str) -> bool:
        query = "INSERT INTO users(telegram_id, role) VALUES($1, $2)"
        return await self.execute_query(query, [user_id, "normal"])

    async def user_exists(self, user_id: str) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1)"
        result = await self.fetch_all(query, [user_id])
        return result[0]["exists"]

    async def user_remove(self, user_id: str) -> bool:
        query = "DELETE FROM users WHERE telegram_id = $1"
        return await self.execute_query(query, [user_id])

    async def add_admin(self, user_id: str) -> bool:
        query = "INSERT INTO users(telegram_id, role) VALUES($1, $2)"
        return await self.execute_query(query, [user_id, "admin"])

    async def check_admin_user(self, user_id: str) -> bool:
        query = (
            "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1 AND role = $2)"
        )
        result = await self.fetch_all(query, [user_id, "admin"])
        return result[0]["exists"]

    async def admin_remove(self, user_id: str) -> bool:
        query = "DELETE FROM users WHERE telegram_id = $1"
        return await self.execute_query(query, [user_id])

    async def add_black_list(self, cmd: str) -> bool:
        query = "INSERT INTO black_list(command) VALUES($1)"
        return await self.execute_query(query, [cmd])

    async def command_exists(self, cmd: str) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM black_list WHERE command = $1)"
        result = await self.fetch_all(query, [cmd])
        return result[0]["exists"]

    async def remove_black_list(self, cmd: str) -> bool:
        query = "DELETE FROM black_list WHERE command = $1"
        return await self.execute_query(query, [cmd])

    async def commands_all(self) -> str:
        query = "SELECT command FROM black_list"
        result = await self.fetch_all(query)
        return "\n".join([row["command"] for row in result])


class DataBase:
    def __init__(self, db_type: str):
        self.db_type = db_type.lower()
        if self.db_type == "sqlite":
            self.database = SqliteDatabase()
        elif self.db_type == "postgresql":
            self.database = PostgresqlDatabase()
        else:
            raise ValueError(
                f"{db_type} - неподдерживаемый тип базы данных.\nИспользуйте PostgreSQL или SQLite"
            )

    async def connect(self) -> None:
        await self.database.connect()

    async def disconnect(self) -> None:
        await self.database.disconnect()

    async def add_user(self, user_id: str) -> bool:
        return await self.database.add_user(user_id)

    async def user_exists(self, user_id: str) -> bool:
        return await self.database.user_exists(user_id)

    async def user_remove(self, user_id: str) -> bool:
        return await self.database.user_remove(user_id)

    async def add_admin(self, user_id: str) -> bool:
        return await self.database.add_admin(user_id)

    async def check_admin_user(self, user_id: str) -> bool:
        return await self.database.check_admin_user(user_id)

    async def admin_remove(self, user_id: str) -> bool:
        return await self.database.admin_remove(user_id)

    async def add_black_list(self, cmd: str) -> bool:
        return await self.database.add_black_list(cmd)

    async def command_exists(self, cmd: str) -> bool:
        return await self.database.command_exists(cmd)

    async def remove_black_list(self, cmd: str) -> bool:
        return await self.database.remove_black_list(cmd)

    async def commands_all(self) -> str:
        return await self.database.commands_all()


db = DataBase(db_type=config.database()["type"])
