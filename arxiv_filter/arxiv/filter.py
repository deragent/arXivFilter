from .scored_entry import scored_entry
from . import util

class filter():

    def __init__(self, definition):

        self._definition = self._cleanDefinition(definition)

    def score(self, entry):

        scored = scored_entry(entry)

        for key in self._definition:

            if key.lower() == 'author':
                score, matches = self._scoreList(self._definition[key], entry.authors)
                if len(matches) > 0:
                    scored.hits['people'] = True
                    scored.score += score
                    scored.matched_authors = matches

            elif key.lower() == 'keyword':
                score, matches = self._scoreString(self._definition[key], entry.title)
                if len(matches) > 0:
                    scored.hits['title'] = True
                    scored.score += score
                    scored.matched_title = matches

                score, matches = self._scoreString(self._definition[key], entry.abstract)
                if len(matches) > 0:
                    scored.hits['abstract'] = True
                    scored.score += score
                    scored.matched_abstract = matches

            elif key.lower() == 'category':
                score, matches = self._scoreList(self._definition[key], entry.categories)
                if len(matches) > 0:
                    scored.hits['category'] = True
                    scored.score += score
                    scored.matched_categories = matches

            elif key.lower() == 'collaboration':
                score, matches = self._scoreString(self._definition[key], entry.collaboration)
                if len(matches) > 0:
                    scored.hits['group'] = True
                    scored.score += score

        return scored


    def _cleanDefinition(self, definition):
        out = {}

        for part, keys in definition.items():
            out[part] = {}
            for key, value in keys.items():
                clean = util.saniztize(key)
                out[part][clean] = int(value)

        return out


    def _scoreList(self, definition, values):
        score = 0
        matches = []

        for item in values:
            clean = util.saniztize(item)
            matched = False

            for key, value in definition.items():
                if key in clean:
                    score += value
                    matched = True

            if matched:
                matches.append(item)


        return score, matches

    def _scoreString(self, definition, string):
        clean, index = util.saniztize(string, return_idx=True)

        score = 0
        matches = []

        for key, value in definition.items():
            if key in clean:
                score += value

                # Extract the match of the original (unsanitized) string
                start = clean.index(key)
                matches.append(string[index[start]:index[start+len(key)-1]+1])

        return score, matches
