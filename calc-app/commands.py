from datetime import datetime
from reports import calc_reports
from calc_ops import calc_op_commands
from input_console import (get_history_entry_id, get_operand,
                           get_history_file_name, get_history_report_file_name)


class AppCommands:

    @staticmethod
    def command_history(history):
        print(calc_reports.display_history(history))
        print(calc_reports.display_operation_counts(history))

    @staticmethod
    def command_remove(history):
        history_entry_id = get_history_entry_id()
        history.remove(history_entry_id)

    @staticmethod
    def command_clear(history):
        history.clear()

    @staticmethod
    def command_calcop_wrapper(command):
        def command_calcop(history):
            num = get_operand()
            # history.append(command, num)
            history += (command, num)
            print(f"Result: {history.result}")
        return command_calcop

    @staticmethod
    def command_save(history):
        history_file_name = get_history_file_name()
        with open(history_file_name, "w") as history_file:
            history_file.write(history.to_json())

    @staticmethod
    def command_load(history):
        history_file_name = get_history_file_name()
        with open(history_file_name, "r") as history_file:
            history.from_json(history_file.read())

    @staticmethod
    def command_save_history_report(history):
        history_report_file_name = get_history_report_file_name()
        with open(history_report_file_name, "w") as history_report_file:
            history_report_file.write(calc_reports.display_history(history))
            history_report_file.write(
                calc_reports.display_operation_counts(history))

    @classmethod
    def build(cls):

        commands = {
            "history": cls.command_history,
            "remove": cls.command_remove,
            "clear": cls.command_clear,
            "save": cls.command_save,
            "load": cls.command_load,
            "save history report": cls.command_save_history_report,
            "noop": lambda *args: None,
        }

        for calc_op_command in calc_op_commands:
            commands[calc_op_command] = cls.command_calcop_wrapper(
                calc_op_command)

        return commands


def command_unknown(*args):
    print("Unknown command. Please try again.")


def log_command(command):
    with open("command.log", "a") as command_log_file:
        command_log_file.write(f"{datetime.now()} {command}\n")


app_commands = AppCommands.build()
