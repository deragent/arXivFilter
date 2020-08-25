import yaml
import os

class DefinitionLoader():

    DEFAULT_LOCATIONS = [
      './',
      '~/.config/',
      '~/',
      '/etc/',
    ]

    FILE_NAME = 'arxiv_filter.yaml'

    def __init__(self):

        self.defintion = {}
        self.error = None

    def loadDefault(self):
        for path in self.DEFAULT_LOCATIONS:
            file = os.path.expanduser(path + self.FILE_NAME)
            if os.path.isfile(file):
                return self.loadFromFile(file)

        self.error = "No default config file (%s) found in [%s]!"%(
            self.FILE_NAME, ', '.join(self.DEFAULT_LOCATIONS))
        return False


    def loadFromFile(self, filename):
        try:
            with open(filename, 'r') as f:
                self.definition = yaml.safe_load(f)
                return True
        except Exception as e:
            self.error = str(e)
            return False
