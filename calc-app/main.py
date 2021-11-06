import argparse
from input_console import get_command
from calc_ops import calc_ops
from models.history import History
from commands import app_commands, command_unknown, log_command


def get_args():

    app_parser = argparse.ArgumentParser(
        description='Console Calculator')

    app_parser.add_argument('history_file_path',
                            type=str,
                            nargs='?',
                            default=None,
                            help='the path to the history file')

    return app_parser.parse_args()


def main():

    args = get_args()

    history = History(calc_ops)

    if args.history_file_path:
        with open(args.history_file_path) as history_file:
            history.from_json(history_file.read())

    command = "noop"

    while command:
        log_command(command)
        command_fn = app_commands.get(command, command_unknown)
        command_fn(history)
        command = get_command()


if __name__ == '__main__':
    main()
