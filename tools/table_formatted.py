from prettytable import PrettyTable

from resources import config


async def get_commands_table_formatted(commands: str) -> str:
    """
    Форматирует список команд в таблицу.

    :param commands: Строка с командами, разделёнными новой строкой.
    :return: Строку с таблицей.
    :rtype: str
    """
    table = PrettyTable()
    table.field_names = config.name_fields_table_list_commands()["name"]

    for command in commands.split("\n"):
        table.add_row([command])

    return table.get_string()
