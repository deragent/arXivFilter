from ..arxiv import util

class DefinitionItem:

    def __init__(self, key, value) -> None:
        self._key = key
        self._exact = False

        # Enable exact matching of a key
        # In this case, the key can not be part of a word!
        if key.startswith('^'):
            self._key = key[1:]
            self._exact = True

        self._clean = util.saniztize(key)
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @property
    def key(self) -> str:
        return self._key

    @property
    def keyClean(self) -> str:
        return self._clean

    @property
    def isExact(self) -> bool:
        return self._exact


class Definition:

    def __init__(self, definiton_data):
        self._data = self._cleanDefinition(definiton_data)

    def _cleanDefinition(self, definiton_data):
        out = {}

        for part, keys in definiton_data.items():
            out[part] = []
            for key, value in keys.items():
                item = DefinitionItem(key, value)
                out[part].append(item)

        return out

    def getCategory(self, category):
        if category in self._data:
            return self._data[category]
        else:
            return {}

    @property
    def categories(self):
        return self._data.keys()
