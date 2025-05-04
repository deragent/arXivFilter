import yaml
import os

from .Definition import Definition

class DefinitionLoader():

    DEFAULT_LOCATIONS = [
      './',
      '~/.config/',
      '~/',
      '/etc/',
    ]

    FILE_NAME = 'arxiv_filter.yaml'

    def __init__(self):

        self.defintion = Definition({})
        self.error = None

    def loadDefault(self):
        """
        Scans all default config file locations for an existing config file.
        """
        for path in self.DEFAULT_LOCATIONS:
            file = os.path.expanduser(path + self.FILE_NAME)
            if os.path.isfile(file):
                return self.loadFromFile(file)

        self.error = "No default config file (%s) found in [%s]!"%(
            self.FILE_NAME, ', '.join(self.DEFAULT_LOCATIONS))
        return False


    def loadFromFile(self, filename):
        """
        Load the filter definition from given filename

        Arguments:
            filename: The file path to load.

        Returns:
            True if definition succesfully loaded, False otherwise.
        """
        try:
            with open(filename, 'r') as f:
                self.definition = Definition(yaml.safe_load(f))
                return True
        except Exception as e:
            self.error = str(e)
            return False
