from prettytable import PrettyTable


async def get_commands_table_formatted(commands: str) -> str:
    table = PrettyTable()
    table.field_names = ["Команды"]

    for command in commands.split("\n"):
        table.add_row([command])

    return table.get_string()
