from .scored_entry import scored_entry
from . import util

class filter():

    def __init__(self, definition) -> None:

        self._definition = definition

    def score(self, entry) -> scored_entry:

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

    def _scoreList(self, category, values) -> tuple[int, list[str]]:
        """
        Score a list of strings according to the given category of the definition.

        Arguments:
            category: The definition category
            values: The list of string to score

        Returns:
            score: The total accumulated score over all entries in values
            matches: List of entries in values which where matched!
        """
        score = 0
        matches = []

        for entry in values:
            clean = util.saniztize(entry)
            matched = False

            for item in self._definition.getCategory(category):
                if not item.isExact:
                    if item.keyClean in clean:
                        # We can do simple matching in this case
                        score += item.value
                        matched = True
                else:
                    # Need more complex mathing for exact matching!
                    pass # TODO

            if matched:
                matches.append(entry)

        return score, matches


    def _scoreString(self, category, string) -> tuple[int, list[str]]:
        """
        Score single text (string) according to the given category of the definition.

        Arguments:
            category: The definition category
            string: The text string to score

        Returns:
            score: The total score of the given text
            matches: List of all substring of the text string which were matched
        """
        clean, index = util.saniztize(string, return_idx=True)

        score = 0
        matches = []

        for item in self._definition.getCategory(category):
            if not item.isExact:
                # We can do simple matching in this case
                if item.keyClean in clean:
                    score += item.value

                    # Extract the match of the original (unsanitized) string
                    start = clean.index(item.keyClean)
                    matches.append(string[index[start]:index[start+len(item.keyClean)-1]+1])
            else:
                # Need more complex mathing for exact matching!
                pass # TODO

        return score, matches
