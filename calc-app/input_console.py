from common.input import input_int, input_float


def get_operand():
    return input_float("Please enter an operand: ")


def get_command():
    return input("Enter a command: ")


def get_history_entry_id():
    return input_int("Please enter a history entry id: ")


def get_history_file_name():
    return input("Enter a history file name: ")


def get_history_report_file_name():
    return input("Enter a history report file name: ")
