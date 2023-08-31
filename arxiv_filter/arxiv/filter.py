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
                score, matches = self._scoreString(self._definition[key], entry.title)
                if score > 0:
                    scored.hits['title'] = True
                    scored.score += score
                    scored.matched_title = matches

                score, matches = self._scoreString(self._definition[key], entry.abstract)
                if score > 0:
                    scored.hits['abstract'] = True
                    scored.score += score
                    scored.matched_abstract = matches

            elif key.lower() == 'category':
                score, matches = self._scoreList(self._definition[key], entry.categories)
                if score > 0:
                    scored.hits['category'] = True
                    scored.score += score
                    scored.matched_categories = matches

            elif key.lower() == 'collaboration':
                score, matches = self._scoreString(self._definition[key], entry.collaboration)
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

    def _sanitize(self, str, returnIdx=False):
        REMOVE = [
            '-', '.', ',', '_', ':', ';',
            '[', ']', '(', ')', '{', '}',
            '^', '\\', '/', '\'', '`', '"', '´',
            '&', '$'
        ]
        REPLACE = {
            'ä': 'a', 'ö': 'o', 'ü': 'u',
            'é': 'e', 'è': 'e', 'à': 'a', 'â': 'a',
        }

        # Replace characters
        clean = str.translate(REPLACE)

        # Remoe characters
        index = []
        output = []

        for cc, char in enumerate(clean):
            if char not in REMOVE:
                output.append(char)
                index.append(cc)

        clean = ''.join(output).lower()

        if not returnIdx:
            return clean
        else:
            return clean, index


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
        clean, index = self._sanitize(string, returnIdx=True)

        score = 0
        matches = []

        for key, value in definition.items():
            if key in clean:
                score += value

                # Extract the match of the original (unsanitized) string
                start = clean.index(key)
                matches.append(string[index[start]:index[start+len(key)-1]+1])

        return score, matches
