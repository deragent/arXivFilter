import email

from .entry import entry

class parser:

    FOOTER_DIVIDER = '%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---%%%---\n'
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

        ## Remove the E-Mail Footer
        parts = str.split(self.FOOTER_DIVIDER)
        if len(parts) < 2:
            self.error = "Error: This is not an arXiv E-Mail!"
            return

        splits = parts[0].split(self.ENTRY_DIVIDER)
        if len(splits) < 2:
            self.warning = "Warning: This does not look like an arXiv E-Mail!"
            pass

        for split in splits:
            if not split.startswith('\\\\'):
                continue

            self._entries.append(entry(split))


    def entries(self):
        return self._entries;
