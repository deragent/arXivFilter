import email

from .entry import entry

class parser:

    FOOTER_DIVIDER = '%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---'
    ENTRY_DIVIDER = '------------------------------------------------------------------------------\n'


    def __init__(self):
        self._entries = []

        self.error = None
        self.warning = None


    def fromEmailFile(self, filename):
        with open(filename, 'r') as f:
            msg = email.message_from_file(f)

        for part in msg.walk():
            # Select the first text/plain entry
            # There should only be one!
            if part.get_content_type() == 'text/plain':
                return self.fromText(part.as_string())
                break;

    def fromEmail(self, str):
        # TODO implement
        pass


    def fromText(self, str):

        ## Unify the line-break character
        # Drap-n-Drop and Copy-Paste might not show the same line-break even on linux!
        str = str.replace("\r\n", "\n")

        ## Remove the E-Mail Footer
        if self.FOOTER_DIVIDER not in str:
            self.warning = "Warning: This might not be an arXiv E-Mail (missing footer)."
        else:
            str = str.split(self.FOOTER_DIVIDER)[0]

        splits = str.split(self.ENTRY_DIVIDER)
        if len(splits) < 2:
            self.warning = "Warning: This might not be an arXiv E-Mail (only one entry)."

        for split in splits:
            if not split.startswith('\\\\'):
                continue

            # TODO better error handling on parse fail
            self._entries.append(entry(split))


    def entries(self):
        return self._entries;
