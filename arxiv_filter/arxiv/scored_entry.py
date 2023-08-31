from .entry import entry

class scored_entry():

    def __init__(self, entry):

        self.entry = entry

        # The keys are chosen, so that all have a different first letter
        # This is used as a shortcut for visualization
        self.hits = {}
        self.hits['people'] = False
        self.hits['group'] = False
        self.hits['title'] = False
        self.hits['abstract'] = False
        self.hits['category'] = False

        self.matched_title = []
        self.matched_abstract = []
        self.matched_authors = []
        self.matched_categories = []

        self.score = 0
