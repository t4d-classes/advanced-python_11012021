"""Provides the History class.

The History class is the primary data structure of the Calc App program. It
stores the history of math operations performed with the calculator.

  Typical usage example:

  history = History(calc_ops)<br>
  history.append("add", 2.0)
"""

from functools import reduce

from mixins.json_mixin import JsonMixin
from models.history_entry import HistoryEntry


class History(JsonMixin):
    """ Manages the operation history

    Attributes:
        _entries: A list of math operation entries.
        _calc_ops: The list of math operations configured for the calculator.
    """

    def __init__(self, calc_ops):
        self._entries = []
        self._calc_ops = calc_ops

    def append(self, entry_op_name, entry_op_value):
        """
        Appends a new history entry to the list of entries.

        Args:
            entry_op_name (str): The name of the operation.
            entry_op_value (float): The value of the operation.

        Returns:
            History: Returns an instance to self.
        """

        next_entry_id = max([entry.id for entry in self._entries] or [0]) + 1

        new_history_entry = HistoryEntry(
            next_entry_id, entry_op_name, entry_op_value)
        self._entries.append(new_history_entry)
        return self

    def remove(self, entry_id):

        for entry in self._entries:
            if entry.id == entry_id:
                self._entries.remove(entry)
                break

        return self

    def clear(self):
        self._entries.clear()

    def _calc_operation(self, result, entry):

        for calc_op in self._calc_ops:
            if entry.op_name == calc_op.command:
                return calc_op.fn(result, entry.op_value)

        return result

    @property
    def result(self):
        return reduce(self._calc_operation, self._entries, 0)

    # def __repr__(self):
    #     return f"Result: {self.result}"

    def __add__(self, history_entry):
        # self.append(history_entry[0], history_entry[1])
        self.append(*history_entry)
        return self

    @property
    def __dict__(self):
        return [entry.__dict__ for entry in self._entries]

    def __len__(self):
        # return self._entries.__len__()
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)

    def __next__(self):
        return next(self._entries)

    @property
    def _data_(self):
        return self._entries

    @_data_.setter
    def _data_(self, entries):
        self._entries = [
            HistoryEntry(
                entry["id"],
                entry["op_name"],
                entry["op_value"]) for entry in entries]
