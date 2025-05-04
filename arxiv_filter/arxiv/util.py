def saniztize(input_string, return_idx=False):
    """
    Sanitize a text string.

    Two main functions:
    - Remove special (non alphabet characters)
    - Replace characters with umlaut, accents etc. with their non-accentuated version.

    Optionally also returns a list of indexes for the sanitized characters into the original string.

    Example:
        INPUT: input_string = "abc/-dé"
        OUTPUT: clean = "abcde"
                index = [0, 1, 2, 5, 6]

    Arguments:
        input_string: The string to be sanitized
        return_idx: If True, the function also returns a list with an entry for
            character in the sanitized string, whith the index of the sanitized
            character in the original string.

    Returns:
        clean: The cleaned (sanitized) output string
        index: If return_idx is True, the index mapping into the original string.
    """

    # Characters to be removed fully.
    REMOVE = [
        '-', '.', ',', '_', ':', ';',
        '[', ']', '(', ')', '{', '}',
        '^', '\\', '/', '\'', '`', '"', '´',
        '&', '$'
    ]
    # Characters to be replaced
    # Only single string replacements are allowed, otherwise index calculation fails!
    REPLACE = {
        'ä': 'a', 'ö': 'o', 'ü': 'u',
        'é': 'e', 'è': 'e', 'à': 'a', 'â': 'a',
    }

    # Replace characters
    clean = input_string.translate(REPLACE)

    # Remove characters
    index = []
    output = []

    # Create the list of characters to keep
    for cc, char in enumerate(clean):
        if char not in REMOVE:
            output.append(char)
            index.append(cc)

    # Join the kept characters back together!
    clean = ''.join(output).lower()

    if not return_idx:
        return clean
    else:
        return clean, index
