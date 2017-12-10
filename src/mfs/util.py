
def n(src):
    """
    Normalize the link. Very basic implementation
    :param src:
    :return:
    """
    if src.startswith('//'):
        src = 'http:' + src
    return src


def sluggify(text):
    """
    Create a file system friendly string from passed text by stripping special characters.
     Use this function to make file names from arbitrary text, like titles
    :param text:
    :return:
    """
    if not text:
        return ''
    return ''.join([c for c in text if c.isalpha() or c.isdigit() or c in [' ', '.', '_', '-', '=']]).rstrip()
