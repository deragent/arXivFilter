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

    def _findAll(self, key, string):
        """
        Return list of all indexes of substring `key` in `string`.

        Overlapping matches of `key` are allowed.
        """
        idx = string.find(key)
        while idx != -1:
            yield idx
            idx = string.find(key, idx+1)


    def findInString(self, string_clean, string_original, mapping):
        """
        Find all locations of the `keyClean` in `string_clean`.
        This functions honours the exact matching if requested!

        Exact matching is implemented by checking characters before and after each match
        in the original (non-sanitized) string `string_original`.
        """
        indexes = self._findAll(self.keyClean, string_clean)
        if not self.isExact:
            # If a non-exact match is ok, we can simply return the clean matches
            return list(indexes)
        else:
            exact_indexes = []
            for idx in indexes:
                index_before = mapping[idx] - 1
                index_after = mapping[idx+len(self.keyClean)-1] + 1

                if index_before >=0  and string_original[index_before].isalpha():
                    # Character before the match is alphabet character
                    continue
                if index_after < len(string_original) and string_original[index_after].isalpha():
                    # Character after the match is alphabet character
                    continue

                exact_indexes.append(idx)

            return exact_indexes



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
