from .entry import entry

class scored_entry():

    def __init__(self, entry):

        self.entry = entry

        self.hits = {}
        self.hits['author'] = False
        self.hits['collaboration'] = False
        self.hits['title'] = False
        self.hits['abstract'] = False
        self.hits['category'] = False

        self.matched_authors = []
        self.matched_categories = []

        self.score = 0
