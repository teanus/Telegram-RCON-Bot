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
from typing import List, Optional

import aiosqlite
import asyncpg
from dotenv import load_dotenv

from resources import config

load_dotenv()


class SqliteDatabase:
    def __init__(self):
        self.con = None

    async def connect(self) -> None:
        """
        Устанавливает соединение с базой данных SQLite и инициализирует таблицы.

        :return: None
        :rtype: None
        """
        try:
            self.con = await aiosqlite.connect(config.sqlite()["name"])
            print("SQLite: connected")
            await self.initialize_tables()
        except aiosqlite.Error as error:
            print(f"Error connecting to the SQLite database: {error}")

    async def disconnect(self) -> None:
        """
        Закрывает соединение с базой данных SQLite.

        :return: None
        :rtype: None
        """
        if self.con:
            await self.con.close()

    async def initialize_tables(self) -> None:
        """
        Инициализирует таблицы в базе данных, если они еще не существуют.

        :return: None
        :rtype: None
        """
        table_users = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY, 
                telegram_id TEXT
            )
        """
        table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
        table_admins = """
            CREATE TABLE IF NOT EXISTS admins(
                id INTEGER PRIMARY KEY,
                telegram_id TEXT
            )
        """
        await self.execute_query(table_users)
        await self.execute_query(table_black_list)
        await self.execute_query(table_admins)
        await self.con.commit()

    async def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """
        Выполняет запрос к базе данных.

        :param query: SQL запрос для выполнения.
        :type query: str
        :param params: Параметры для запроса.
        :type params: Optional[tuple]
        :return: Успешность выполнения запроса.
        :rtype: bool
        """
        try:
            if not self.con:
                await self.connect()
            async with self.con.execute(query, params or ()):
                pass
            await self.con.commit()
            return True
        except aiosqlite.Error as error:
            print(f"Error executing SQLite query: {error}")
            return False

    async def fetch_all(
        self, query: str, params: Optional[tuple] = None
    ) -> List[tuple]:
        """
        Выполняет запрос к базе данных и возвращает все результаты.

        :param query: SQL запрос для выполнения.
        :type query: str
        :param params: Параметры для запроса.
        :type params: Optional[tuple]
        :return: Список строк результата запроса.
        :rtype: List[tuple]
        """
        try:
            if not self.con:
                await self.connect()
            async with self.con.execute(query, params or ()) as cursor:
                result = await cursor.fetchall()
            return result
        except aiosqlite.Error as error:
            print(f"Error executing SQLite query: {error}")
            return []

    async def add_user(self, user_id: str) -> bool:
        """
        Добавляет пользователя в таблицу пользователей.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Успешность добавления пользователя.
        :rtype: bool
        """
        query = "INSERT INTO users(telegram_id) VALUES(?)"
        return await self.execute_query(query, (user_id,))

    async def user_exists(self, user_id: str) -> bool:
        """
        Проверяет, существует ли пользователь в базе данных.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Существует ли пользователь.
        :rtype: bool
        """
        query = "SELECT 1 FROM users WHERE telegram_id = ?"
        result = await self.fetch_all(query, (user_id,))
        return bool(result)

    async def user_remove(self, user_id: str) -> bool:
        """
        Удаляет пользователя из таблицы пользователей.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Успешность удаления пользователя.
        :rtype: bool
        """
        query = "DELETE FROM users WHERE telegram_id = ?"
        return await self.execute_query(query, (user_id,))

    async def add_admin(self, user_id: str) -> bool:
        """
        Добавляет администратора в таблицу администраторов.

        :param user_id: Идентификатор администратора.
        :type user_id: str
        :return: Успешность добавления администратора.
        :rtype: bool
        """
        query = "INSERT INTO admins(telegram_id) VALUES(?)"
        return await self.execute_query(query, (user_id,))

    async def check_admin(self, user_id: str) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Является ли пользователь администратором.
        :rtype: bool
        """
        query = "SELECT 1 FROM admins WHERE telegram_id = ?"
        result = await self.fetch_all(query, (user_id,))
        return bool(result)

    async def admin_remove(self, user_id: str) -> bool:
        """
        Удаляет администратора из таблицы администраторов.

        :param user_id: Идентификатор администратора.
        :type user_id: str
        :return: Успешность удаления администратора.
        :rtype: bool
        """
        query = "DELETE FROM admins WHERE telegram_id = ?"
        return await self.execute_query(query, (user_id,))

    async def add_black_list(self, command: str) -> bool:
        """
        Добавляет команду в черный список.

        :param command: Команда для добавления в черный список.
        :type command: str
        :return: Успешность добавления команды в черный список.
        :rtype: bool
        """
        query = "INSERT INTO black_list(command) VALUES(?)"
        return await self.execute_query(query, (command,))

    async def remove_black_list(self, command: str) -> bool:
        """
        Удаляет команду из черного списка.

        :param command: Команда для удаления из черного списка.
        :type command: str
        :return: Успешность удаления команды из черного списка.
        :rtype: bool
        """
        query = "DELETE FROM black_list WHERE command = ?"
        return await self.execute_query(query, (command,))

    async def command_exists(self, command: str) -> bool:
        """
        Проверяет, существует ли команда в черном списке.

        :param command: Команда для проверки.
        :type command: str
        :return: Существует ли команда в черном списке.
        :rtype: bool
        """
        query = "SELECT 1 FROM black_list WHERE command = ?"
        result = await self.fetch_all(query, (command,))
        return bool(result)

    async def commands_all(self) -> str:
        """
        Возвращает все команды из черного списка.

        :return: Список команд из черного списка в виде строки.
        :rtype: str
        """
        query = "SELECT command FROM black_list"
        result = await self.fetch_all(query)
        return "\n".join([row[0] for row in result])


class PostgresqlDatabase:
    def __init__(self):
        self.con = None

    async def connect(self) -> None:
        """
        Устанавливает соединение с базой данных PostgreSQL и инициализирует таблицы.

        :return: None
        :rtype: None
        """
        try:
            self.con = await asyncpg.connect(
                user=getenv("postgre_username"),
                password=getenv("postgre_password"),
                database=getenv("postgre_database_name"),
                host=getenv("postgre_host"),
                port=getenv("postgre_port"),
            )
            print("PostgreSQL: connected")
            await self.initialize_tables()
        except asyncpg.PostgresError as error:
            print(f"Error connecting to the postgresql database: {error}")

    async def disconnect(self) -> None:
        """
        Закрывает соединение с базой данных PostgreSQL.

        :return: None
        :rtype: None
        """
        if self.con:
            await self.con.close()

    async def initialize_tables(self) -> None:
        """
        Инициализирует таблицы в базе данных, если они еще не существуют.

        :return: None
        :rtype: None
        """
        table_users = """
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY, 
                telegram_id TEXT, 
            )
        """
        table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
        table_admins = """
            CREATE TABLE IF NOT EXISTS admins(
                id SERIAL PRIMARY KEY,
                telegram_id TEXT
            )
        """
        await self.execute_query(table_users)
        await self.execute_query(table_black_list)
        await self.execute_query(table_admins)
        await self.con.commit()

    async def execute_query(self, query: str, params: Optional[List] = None) -> bool:
        """
        Выполняет запрос к базе данных.

        :param query: SQL запрос для выполнения.
        :type query: str
        :param params: Параметры для запроса.
        :type params: Optional[List]
        :return: Успешность выполнения запроса.
        :rtype: bool
        """
        try:
            if not self.con:
                await self.connect()
            await self.con.execute(query, *params or ())
            await self.con.commit()
            return True
        except asyncpg.PostgresError as error:
            print(f"Error executing PostgreSQL query: {error}")
            return False

    async def fetch_all(self, query: str, params: Optional[List] = None) -> List[dict]:
        """
        Выполняет запрос к базе данных и возвращает все результаты.

        :param query: SQL запрос для выполнения.
        :type query: str
        :param params: Параметры для запроса.
        :type params: Optional[List]
        :return: Список строк результата запроса.
        :rtype: List[dict]
        """
        try:
            if not self.con:
                await self.connect()
            result = await self.con.fetch(query, *params or ())
            return result
        except asyncpg.PostgresError as error:
            print(f"Error executing PostgreSQL query: {error}")
            return []

    async def add_user(self, user_id: str) -> bool:
        """
        Добавляет пользователя в таблицу пользователей.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Успешность добавления пользователя.
        :rtype: bool
        """
        query = "INSERT INTO users(telegram_id) VALUES($1)"
        return await self.execute_query(query, [user_id])

    async def user_exists(self, user_id: str) -> bool:
        """
        Проверяет, существует ли пользователь в базе данных.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Существует ли пользователь.
        :rtype: bool
        """
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1)"
        result = await self.fetch_all(query, [user_id])
        return result[0]["exists"]

    async def user_remove(self, user_id: str) -> bool:
        """
        Удаляет пользователя из таблицы пользователей.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Успешность удаления пользователя.
        :rtype: bool
        """
        query = "DELETE FROM users WHERE telegram_id = $1"
        return await self.execute_query(query, [user_id])

    async def add_admin(self, user_id: str) -> bool:
        """
        Добавляет администратора в таблицу администраторов.

        :param user_id: Идентификатор администратора.
        :type user_id: str
        :return: Успешность добавления администратора.
        :rtype: bool
        """
        query = "INSERT INTO admins(telegram_id) VALUES($1)"
        return await self.execute_query(query, [user_id])

    async def check_admin(self, user_id: str) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Является ли пользователь администратором.
        :rtype: bool
        """
        query = "SELECT EXISTS(SELECT 1 FROM admins WHERE telegram_id = $1)"
        result = await self.fetch_all(query, [user_id])
        return result[0]["exists"]

    async def admin_remove(self, user_id: str) -> bool:
        """
        Удаляет администратора из таблицы администраторов.

        :param user_id: Идентификатор администратора.
        :type user_id: str
        :return: Успешность удаления администратора.
        :rtype: bool
        """
        query = "DELETE FROM admins WHERE telegram_id = $1"
        return await self.execute_query(query, [user_id])

    async def add_black_list(self, command: str) -> bool:
        """
        Добавляет команду в черный список.

        :param command: Команда для добавления в черный список.
        :type command: str
        :return: Успешность добавления команды в черный список.
        :rtype: bool
        """
        query = "INSERT INTO black_list(command) VALUES($1)"
        return await self.execute_query(query, [command])

    async def command_exists(self, command: str) -> bool:
        """
        Проверяет, существует ли команда в черном списке.

        :param command: Команда для проверки.
        :type command: str
        :return: Существует ли команда в черном списке.
        :rtype: bool
        """
        query = "SELECT EXISTS(SELECT 1 FROM black_list WHERE command = $1)"
        result = await self.fetch_all(query, [command])
        return result[0]["exists"]

    async def remove_black_list(self, command: str) -> bool:
        """
        Удаляет команду из черного списка.

        :param command: Команда для удаления из черного списка.
        :type command: str
        :return: Успешность удаления команды из черного списка.
        :rtype: bool
        """
        query = "DELETE FROM black_list WHERE command = $1"
        return await self.execute_query(query, [command])

    async def commands_all(self) -> str:
        """
        Возвращает все команды из черного списка.

        :return: Список команд из черного списка в виде строки.
        :rtype: str
        """
        query = "SELECT command FROM black_list"
        result = await self.fetch_all(query)
        return "\n".join([row["command"] for row in result])


class DataBase:
    def __init__(self, db_type: str):
        """
        Инициализирует объект базы данных в зависимости от указанного типа.

        :param db_type: Тип базы данных ('sqlite' или 'postgresql').
        :type db_type: str
        :raises ValueError: Если указан неподдерживаемый тип базы данных.
        """
        self.db_type = db_type.lower()
        if self.db_type == "sqlite":
            self.database = SqliteDatabase()
        elif self.db_type == "postgresql":
            self.database = PostgresqlDatabase()
        else:
            raise ValueError(
                f"{db_type} - Unsupported database type. Please use PostgreSQL or SQLite."
            )

    async def connect(self) -> None:
        """
        Устанавливает соединение с базой данных.

        :return: None
        :rtype: None
        """
        await self.database.connect()

    async def disconnect(self) -> None:
        """
        Закрывает соединение с базой данных.

        :return: None
        :rtype: None
        """
        await self.database.disconnect()

    async def add_user(self, user_id: str) -> bool:
        """
        Добавляет пользователя в базу данных.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Успешность добавления пользователя.
        :rtype: bool
        """
        return await self.database.add_user(user_id)

    async def user_remove(self, user_id: str) -> bool:
        """
        Удаляет пользователя из базы данных.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Успешность удаления пользователя.
        :rtype: bool
        """
        return await self.database.user_remove(user_id)

    async def user_exists(self, user_id: str) -> bool:
        """
        Проверяет, существует ли пользователь в базе данных.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Существует ли пользователь.
        :rtype: bool
        """
        return await self.database.user_exists(user_id)

    async def add_admin(self, user_id: str) -> bool:
        """
        Добавляет администратора в базу данных.

        :param user_id: Идентификатор администратора.
        :type user_id: str
        :return: Успешность добавления администратора.
        :rtype: bool
        """
        return await self.database.add_admin(user_id)

    async def admin_remove(self, user_id: str) -> bool:
        """
        Удаляет администратора из базы данных.

        :param user_id: Идентификатор администратора.
        :type user_id: str
        :return: Успешность удаления администратора.
        :rtype: bool
        """
        return await self.database.admin_remove(user_id)

    async def check_admin(self, user_id: str) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        :param user_id: Идентификатор пользователя.
        :type user_id: str
        :return: Является ли пользователь администратором.
        :rtype: bool
        """
        return await self.database.check_admin(user_id)

    async def add_black_list(self, command: str) -> bool:
        """
        Добавляет команду в черный список.

        :param command: Команда для добавления в черный список.
        :type command: str
        :return: Успешность добавления команды в черный список.
        :rtype: bool
        """
        return await self.database.add_black_list(command)

    async def remove_black_list(self, command: str) -> bool:
        """
        Удаляет команду из черного списка.

        :param command: Команда для удаления из черного списка.
        :type command: str
        :return: Успешность удаления команды из черного списка.
        :rtype: bool
        """
        return await self.database.remove_black_list(command)

    async def command_exists(self, command: str) -> bool:
        """
        Проверяет, существует ли команда в черном списке.

        :param command: Команда для проверки.
        :type command: str
        :return: Существует ли команда в черном списке.
        :rtype: bool
        """
        return await self.database.command_exists(command)

    async def commands_all(self) -> str:
        """
        Возвращает все команды из черного списка.

        :return: Список команд из черного списка в виде строки.
        :rtype: str
        """
        return await self.database.commands_all()


db = DataBase(db_type=config.database()["type"])
