from .scored_entry import scored_entry

class filter():

    def __init__(self, definition):

        self._definition = self._cleanDefinition(definition)

    def score(self, entry):

        scored = scored_entry(entry)

        for key in self._definition:

            if key.lower() == 'author':
                score, matches = self._scoreList(self._definition[key], entry.authors)
                if score > 0:
                    scored.hits['people'] = True
                    scored.score += score
                    scored.matched_authors = matches

            elif key.lower() == 'keyword':
                score = self._scoreString(self._definition[key], entry.title)
                if score > 0:
                    scored.hits['title'] = True
                    scored.score += score

                score = self._scoreString(self._definition[key], entry.abstract)
                if score > 0:
                    scored.hits['abstract'] = True
                    scored.score += score

            elif key.lower() == 'category':
                score, matches = self._scoreList(self._definition[key], entry.categories)
                if score > 0:
                    scored.hits['category'] = True
                    scored.score += score
                    scored.matched_categories = matches

            elif key.lower() == 'collaboration':
                score = self._scoreString(self._definition[key], entry.collaboration)
                if score > 0:
                    scored.hits['group'] = True
                    scored.score += score

        return scored


    def _cleanDefinition(self, definition):
        out = {}

        for part, keys in definition.items():
            out[part] = {}
            for key, value in keys.items():
                clean = self._sanitize(key)
                out[part][clean] = int(value)

        return out

    def _sanitize(self, str):
        str = str.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')
        str = str.replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('â', 'a')

        str = str.replace('-', '').replace('.', '').replace(',', '').replace('_', '').replace(':', '').replace(';', '')
        str = str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('{', '').replace('}', '')
        str = str.replace('^', '').replace('\'', '').replace('`', '').replace('"', '').replace('´', '').replace('&', '')

        return str.lower()


    def _scoreList(self, definition, values):
        score = 0
        matches = []

        for item in values:
            clean = self._sanitize(item)
            matched = False

            for key, value in definition.items():
                if key in clean:
                    score += value
                    matched = True

            if matched:
                matches.append(item)


        return score, matches

    def _scoreString(self, definition, string):
        clean = self._sanitize(string)

        score = 0
        for key, value in definition.items():
            if key in clean:
                score += value

        return score
