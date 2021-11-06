from calc_ops import calc_ops
from common.text_view import display_table


def display_operation_counts(history):

    calc_op_counts = []

    for calc_op in calc_ops:

        op_count = len([entry for entry in history
                        if entry.op_name == calc_op.command])

        calc_op_counts.append({
            "op_counts": f"{calc_op.label}: {op_count}"
        })

    return display_table(
        [("Op Counts", "op_counts", 15)], calc_op_counts)


def display_history(history):

    return display_table([
        ("Id", "id", 2),
        ("Op Name", "op_name", 10),
        ("Op Value", "op_value", 10),
    ], (history.__dict__))
