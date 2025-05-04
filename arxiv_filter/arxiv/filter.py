from .scored_entry import scored_entry
from . import util

class filter():

    def __init__(self, definition):

        self._definition = definition

    def score(self, entry):

        scored = scored_entry(entry)

        for category in self._definition.categories:

            if category.lower() == 'author':
                score, matches = self._scoreList(category, entry.authors)
                if len(matches) > 0:
                    scored.hits['people'] = True
                    scored.score += score
                    scored.matched_authors = matches

            elif category.lower() == 'keyword':
                score, matches = self._scoreString(category, entry.title)
                if len(matches) > 0:
                    scored.hits['title'] = True
                    scored.score += score
                    scored.matched_title = matches

                score, matches = self._scoreString(category, entry.abstract)
                if len(matches) > 0:
                    scored.hits['abstract'] = True
                    scored.score += score
                    scored.matched_abstract = matches

            elif category.lower() == 'category':
                score, matches = self._scoreList(category, entry.categories)
                if len(matches) > 0:
                    scored.hits['category'] = True
                    scored.score += score
                    scored.matched_categories = matches

            elif category.lower() == 'collaboration':
                score, matches = self._scoreString(category, entry.collaboration)
                if len(matches) > 0:
                    scored.hits['group'] = True
                    scored.score += score

        return scored

    def _scoreList(self, category, values):
        score = 0
        matches = []

        for item in values:
            clean = util.saniztize(item)
            matched = False

            for key, value in self._definition.getCategory(category).items():
                if key in clean:
                    score += value
                    matched = True

            if matched:
                matches.append(item)


        return score, matches

    def _scoreString(self, category, string):
        clean, index = util.saniztize(string, return_idx=True)

        score = 0
        matches = []

        for key, value in self._definition.getCategory(category).items():
            if key in clean:
                score += value

                # Extract the match of the original (unsanitized) string
                start = clean.index(key)
                matches.append(string[index[start]:index[start+len(key)-1]+1])

        return score, matches
