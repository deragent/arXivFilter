from datetime import datetime
import re

class entry:

    DATEFORMAT = '%d %b %Y %H:%M:%S %Z'

    def __str__(self):
        pass

    def __init__(self, entry_str):

        self.abstract = ''
        self.link = ''
        self.size = ''

        self.key = ''
        self.date = None

        self.title = ''

        self.authors = []
        self.collaboration = ''

        self.categories = []
        self.doi = ''
        self.new = True

        parts = entry_str.split('\\\\')

        for part in parts:
            if part.startswith('\narXiv:'):
                self.parseHeader(part)
            elif part.startswith(' ( '):
                self.parseFooter(part)
            else:
                self.parseAbstract(part)


    def parseHeader(self, data):

        data = data.replace('\n  ', ' ')
        headers = data.split('\n')


        for header in headers:
            header = header.strip()
            if header == '':
                continue

            if header.startswith('replaced with'):
                self.parseDateStr(header)
                self.new = False
                continue

            if header.startswith('Date:'):
                self.parseDateStr(header)
                continue

            try:
                key, value = header.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
            except Exception as e:
                print(header)
                print('Warning: ' + str(e))
                continue

            if key == 'title':
                self.title = value
            elif key == 'authors':
                self.parseAuthors(value)
            elif key == 'categories':
                self.categories = value.split(' ')
            elif key == 'doi':
                self.doi = value
            elif key == 'arxiv':
                self.parseKey(value)

            ## TODO support more metadata


    def _sanitize(self, str):
        return str.replace('\\"a', 'ä').replace('\\"u', 'ü').replace('\\"o', 'ö').replace('\\`e', 'è').replace('\\\'e', 'é')


    def parseAbstract(self, data):
        abstract = ' '.join(data.strip().split('\n'))

        # Replace some common latex umlaut notations
        self.abstract = self._sanitize(abstract)


    def parseFooter(self, data):
        data = data.replace('(', '').replace(')', '')

        parts = data.split(',')
        if len(parts) < 2:
            # TOOD raise exception
            return

        self.link = parts[0].strip()
        self.size = parts[1].strip()



    def parseAuthors(self, authorstr):

        authorstr = self._sanitize(authorstr)

        authors = authorstr.strip().split(',')

        # Extract the collaboration at the front
        if ': ' in authors[0]:
            front = authors[0].split(': ', 1)

            self.collaboration = front[0].strip()
            authors[0] = front[1].strip()
        elif 'collaboration' in authors[0].lower():
            self.collaboration = authors[0]
            authors = authors[1:]

        # Split last author on 'and'
        if len(authors) > 0 and ' and ' in authors[-1]:
            back = authors[-1].split(' and ', 1)
            authors[-1] = back[0]
            authors.append(back[1])

        # This is a very basic author extraction
        # This could very likely be improved in the future for additional
        # edge cases.

        self.authors = [a.strip() for a in authors if len(a.strip()) > 0]

    def parseDateStr(self, datestr):
        try:
            date = re.match(".*, ([^\(]*)\(.*", datestr)
            if date:
                self.date = datetime.strptime(date.groups()[0].strip(), self.DATEFORMAT)
        except Exception as e:
            # TODO better error handling!
            print(e)
            pass

    def parseKey(self, keystr):
        try:
            parts = keystr.strip().split(' ')
            self.key = parts[0]
        except:
            pass
