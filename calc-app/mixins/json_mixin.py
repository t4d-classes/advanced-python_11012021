import json


class JsonMixin:

    def to_json(self):
        # [ HistoryEntry(), HistoryEntry(), HistoryEntry() ]
        return json.dumps(self._data_, indent=2, default=lambda o: o.__dict__)

    def from_json(self, json_data):
        self._data_ = json.loads(json_data)
