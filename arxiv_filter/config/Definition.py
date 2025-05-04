from ..arxiv import util

class Definition:

    def __init__(self, definiton_data):
        self._data = self._cleanDefinition(definiton_data)

    def _cleanDefinition(self, definiton_data):
        out = {}

        for part, keys in definiton_data.items():
            out[part] = {}
            for key, value in keys.items():
                clean = util.saniztize(key)
                out[part][clean] = int(value)

        return out

    def getCategory(self, category):
        if category in self._data:
            return self._data[category]
        else:
            return {}

    @property
    def categories(self):
        return self._data.keys()
